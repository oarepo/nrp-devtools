from . import build_command
from ..commands.invenio import install_invenio_cfg
from ..commands.pdm import build_requirements, install_python_repository, clean_previous_installation, create_empty_venv
from ..commands.ui.assets import collect_assets, install_npm_packages
from ..commands.ui.build import build_production_ui
from ..commands.utils import make_step
from ..config import OARepoConfig
from .base import command_sequence, nrp_command


@nrp_command.command(name="upgrade")
@command_sequence()
def upgrade_command(*, config: OARepoConfig, **kwargs):
    """Upgrades the repository.

    Resolves the newest applicable packages, downloads them and rebuilds the repository.
    """
    return (
        build_requirements,
    ) + build_command(config=config)
