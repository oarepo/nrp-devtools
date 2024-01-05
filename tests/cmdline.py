import os
import select
import subprocess
import re
import sys
import time

import click

from nrp_cli.commands.pdm import remove_virtualenv_from_env


class CommandLineTester:
    def __init__(self, command, *args, environment=None, cwd=None):
        self.command = command
        self.args = args
        self.environment = environment or {}
        self.cwd = cwd
        self.process = None

    def start(self):
        click.secho(f"Starting {self.command} {' '.join(self.args)} inside {self.cwd}", fg="yellow")
        self.process = subprocess.Popen(
            [self.command, *self.args],
            env={**remove_virtualenv_from_env(), **self.environment},
            cwd=self.cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        os.set_blocking(self.process.stdout.fileno(), False)
        os.set_blocking(self.process.stderr.fileno(), False)
        return self

    def stop(self):
        self.running = False
        self.process.terminate()
        self.process.wait(3)
        if self.process.poll() is None:
            self.process.kill()
        return self

    def expect(self, regexp_line_str, timeout=5, stdout=True):
        stream = self.process.stdout if stdout else self.process.stderr
        other_stream = self.process.stderr if stdout else self.process.stdout

        streams = [stream, other_stream]

        start = time.time()
        last_line = b""
        regexp_line = re.compile(regexp_line_str)
        while True:
            current = time.time()

            if current - start > timeout:
                raise AssertionError(f"Expected line {regexp_line_str} not found.")

            selected = select.select(streams, [], [], 1)

            if stream in selected[0]:
                # not very efficient, but we don't expect a lot of output in tests
                while True:
                    c = stream.read(1)
                    if not c:
                        break

                    if stdout:
                        sys.stdout.buffer.write(c)
                        sys.stdout.flush()
                    else:
                        sys.stderr.buffer.write(c)
                        sys.stderr.flush()

                    if c == b"\n":
                        last_line = b""
                        continue

                    last_line += c
                    try:
                        ll = last_line.decode("utf-8")
                        if regexp_line.search(ll):
                            return True
                    except UnicodeDecodeError:
                        pass

            # output other stream
            if other_stream in selected[0]:
                if stdout:
                    sys.stderr.buffer.write(other_stream.read())
                    sys.stderr.flush()
                else:
                    sys.stdout.buffer.write(other_stream.read())
                    sys.stdout.flush()

    def enter(self, line, eol=True):
        sys.stdout.flush()
        sys.stderr.flush()
        print(line, flush=True)

        self.process.stdin.write(line.encode("utf-8"))
        if eol:
            self.process.stdin.write(b"\n")

        self.process.stdin.flush()
        return self

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting")
        self.stop()

    def wait_for_exit(self, timeout=5):
        start = time.time()
        while True:
            current = time.time()

            if current - start > timeout:
                raise AssertionError(f"Process did not exit in {timeout} seconds.")

            sys.stdout.buffer.write(self.process.stdout.read() or b"")
            sys.stderr.buffer.write(self.process.stderr.read() or b"")

            if self.process.poll() is not None:
                return

            time.sleep(0.1)
