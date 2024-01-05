import json
import re
from pathlib import Path

from nrp_devtools.commands.utils import run_cmdline
from nrp_devtools.config import OARepoConfig


def register_less_components(config: OARepoConfig, invenio_instance_path):
    run_cmdline(
        config.invenio_command,
        "oarepo",
        "assets",
        "less-components",
        f"{invenio_instance_path}/less-components.json",
    )
    data = json.loads(Path(f"{invenio_instance_path}/less-components.json").read_text())
    components = list(set(data["components"]))
    theme_config_file = (
        config.ui_dir / "branding" / config.theme_dir_name / "less" / "theme.config"
    )
    theme_data = theme_config_file.read_text()
    for c in components:
        match = re.search("^@" + c, theme_data, re.MULTILINE)
        if not match:
            match = theme_data.index("/* @my_custom_component : 'default'; */")
            theme_data = (
                theme_data[:match] + f"\n@{c}: 'default';\n" + theme_data[match:]
            )
    theme_config_file.write_text(theme_data)
