from oarepo_ui.resources.components import BabelComponent, FilesComponent
from oarepo_ui.resources.config import RecordsUIResourceConfig
from oarepo_ui.resources.resource import RecordsUIResource


class {{cookiecutter.resource_config}}(RecordsUIResourceConfig):
    template_folder = "templates"
    url_prefix = "{{cookiecutter.endpoint}}"
    blueprint_name = "{{cookiecutter.name}}"
    ui_serializer_class = "{{cookiecutter.ui_serializer_class}}"
    api_service = "{{cookiecutter.api_service}}"

    components = [BabelComponent, FilesComponent]
    try:
        from oarepo_vocabularies.ui.resources.components import (
            DepositVocabularyOptionsComponent,
        )
        components.append(DepositVocabularyOptionsComponent)
    except ImportError:
        pass

    application_id="{{cookiecutter.name}}"

    templates = {
        "detail": "{{cookiecutter.name}}.Detail",
        "search": "{{cookiecutter.name}}.Search",
        "edit": "{{cookiecutter.name}}.Deposit",
        "create":"{{cookiecutter.name}}.Deposit",
    }


class {{cookiecutter.resource}}(RecordsUIResource):
    pass


def create_blueprint(app):
    """Register blueprint for this resource."""
    return {{cookiecutter.resource}}({{cookiecutter.resource_config}}()).as_blueprint()
