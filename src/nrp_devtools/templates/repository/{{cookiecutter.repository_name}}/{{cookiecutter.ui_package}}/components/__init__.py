from oarepo_ui.resources import UIResourceConfig
from oarepo_ui.resources.resource import TemplatePageUIResource


class ComponentsResourceConfig(UIResourceConfig):
    url_prefix = "/"
    blueprint_name = "components"
    template_folder = "templates"


def create_blueprint(app):
    """Register blueprint for this resource."""
    return TemplatePageUIResource(ComponentsResourceConfig()).as_blueprint()
