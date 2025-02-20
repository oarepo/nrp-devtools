import dataclasses
import os
import sys
from pathlib import Path

import click
import copier
import yaml

from ..config import OARepoConfig
from ..config.repository_config import RepositoryConfig
from ..x509 import generate_selfsigned_cert
from .base import command_sequence, nrp_command


@nrp_command.command(name="initialize")
@click.option(
    "--initial-config",
    default=None,
    help="Initial configuration file",
    type=click.Path(exists=True),
)
@click.option(
    "--no-input",
    default=None,
    help="Do not ask for input, use the initial config only",
    is_flag=True,
)
@command_sequence(
    repository_dir_as_argument=True, repository_dir_must_exist=False, save=True
)
def initialize_command(
    *,
    repository_dir: Path,
    config: OARepoConfig,
    verbose: bool,
    initial_config: Path,
    no_input: bool,
):
    """
    Initialize a new nrp project. Note: the project directory must be empty.
    """
    if repository_dir.exists() and len(list(repository_dir.iterdir())) > 0:
        click.secho(
            f"Project directory {repository_dir} must be empty", fg="red", err=True
        )
        sys.exit(1)

    def initialize_step(config: OARepoConfig):
        if initial_config:
            config.load(Path(initial_config))

        template_path = os.environ.get("NRP_APP_TEMPLATE", "gh:oarepo/nrp-app-copier")
        initial_data = (
            dataclasses.asdict(config.repository) if config.repository else None
        )
        copier.run_copy(template_path, repository_dir, initial_data, unsafe=True)
        answer_file = repository_dir / ".copier-answers.yml"
        with answer_file.open("r") as f:
            data: dict[str, str] = yaml.safe_load(f)
            config.repository = RepositoryConfig(
                repository_human_name=data["repository_human_name"].strip(),
                repository_name=data["repository_name"].strip(),
                repository_description=data["repository_description"].strip(),
                languages=[
                    x.strip() for x in data["languages"].strip().split(",") if x.strip()
                ],
            )
            config.i18n.languages = ["en"] + data["languages"].split(",")

    def generate_certificate_step(config: OARepoConfig):
        # generate the certificate
        cert, key = generate_selfsigned_cert("localhost", ["127.0.0.1"])
        (config.repository_dir / "docker" / "development.crt").write_bytes(cert)
        (config.repository_dir / "docker" / "development.key").write_bytes(key)

    def link_variables_step(config: OARepoConfig):
        # link the variables
        (config.repository_dir / "docker" / ".env").symlink_to(
            config.repository_dir / "variables"
        )

    def mark_nrp_executable_step(config: OARepoConfig):
        # mark the nrp command executable
        (config.repository_dir / "nrp").chmod(0o755)

    def set_up_i18n_step(config: OARepoConfig):
        # set up the i18n
        config.i18n.babel_source_paths = [
            "common",
            "ui",
        ]
        config.i18n.i18next_source_paths = ["ui"]

    return (
        initialize_step,
        generate_certificate_step,
        link_variables_step,
        mark_nrp_executable_step,
        set_up_i18n_step,
    )
