import json
import shutil
from pathlib import Path

from nrp_devtools.commands.ui import register_less_components
from nrp_devtools.commands.utils import run_cmdline


def load_watched_paths(paths_json, extra_paths):
    watched_paths = {}
    with open(paths_json) as f:
        for target, paths in json.load(f).items():
            if target.startswith("@"):
                continue
            for pth in paths:
                watched_paths[pth] = target
    for e in extra_paths:
        source, target = e.split("=", maxsplit=1)
        watched_paths[source] = target
    return watched_paths


def collect_assets(config):
    invenio_instance_path = config.invenio_instance_path
    shutil.rmtree(invenio_instance_path / "assets", ignore_errors=True)
    shutil.rmtree(invenio_instance_path / "static", ignore_errors=True)
    Path(invenio_instance_path / "assets").mkdir(parents=True)
    Path(invenio_instance_path / "static").mkdir(parents=True)
    register_less_components(config, invenio_instance_path)
    run_cmdline(
        config.invenio_command,
        "oarepo",
        "assets",
        "collect",
        f"{invenio_instance_path}/watch.list.json",
    )
    run_cmdline(
        config.invenio_command,
        "webpack",
        "clean",
        "create",
    )
    # shutil.copytree(
    #     config.site_dir / "assets", invenio_instance_path / "assets", dirs_exist_ok=True
    # )
    # shutil.copytree(
    #     config.site_dir / "static", invenio_instance_path / "static", dirs_exist_ok=True
    # )


def install_npm_packages(config):
    run_cmdline(
        config.invenio_command,
        "webpack",
        "install",
    )
