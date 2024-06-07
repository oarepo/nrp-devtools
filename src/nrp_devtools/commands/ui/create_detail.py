import json
from pathlib import Path
import pydash


def create_detail_page(ui_file, target_dir: Path, prefix):
    prefix = prefix.capitalize()
    ui_data = json.loads(Path(ui_file).read_text())
    if 'metadata' in ui_data['children']:
        in_metadata = True
        root = ui_data['children']['metadata']
    else:
        in_metadata = False
        root = ui_data
    generate_jinjax_root_component(root, in_metadata, target_dir, prefix)

def generate_jinjax_root_component(root, in_metadata, target_dir: Path, prefix):
    output = [
        "{# def d, level=0 #}",
    ]
    if in_metadata:
        output.append("{% set md=d.metadata %}")
    else:
        output.append("{% set md=d %}")
    output.append("")

    add_depth(root)
    primitive, complex = pydash.partition(root['children'].items(), lambda x: x[1]['depth'] == 0)
    output.append("<ITable>")
    for key, value in primitive:
        if not is_array(value):
            output.append("  <ITableField d={md.%s} />" % key)
        else:
            output.append("  <ITableField d={md.%s} >" % key)
            output.append("    <ITableArrayValue value={md.%s} />" % key)
            output.append("  </ITableField>")

    # complex values will be rendered as an ISection component
    for key, value in complex:

        component_name, generate, add_field = jinja_component_name(prefix, value)
        if not component_name:
            continue
        if generate:
            generate_jinjax_component(value if not is_array(value) else value['child'],
                                      target_dir, component_name, prefix)

        if not is_array(value):
            if add_field:
                output.append("  <ITableField d={md.%s} >" % key)
            output.append("  <%s d={md.%s} level={level+1}/>" % (component_name, key))
            if add_field:
                output.append("  </ITableField>")
        else:
            output.append("  {%% for item in array(md.%s) %%}" % key)
            if add_field:
                output.append("    <ITableField d={item} >")
            output.append("      <%s d={item} level={level+1}/>" % component_name)
            if add_field:
                output.append("    </ITableField>")
            output.append("  {% endfor %}")

    output.append("</ITable>")
    (target_dir / f'{prefix}DetailRoot.jinja').write_text('\n'.join(output))


def generate_jinjax_component(data, target_dir: Path, name, prefix):
    output = [
        "{# def d, level=0 #}",
        ""
        "<ITableSection level={level} title={d._ui_label} >"
    ]

    primitive, complex = pydash.partition(data['children'].items(), lambda x: x[1]['depth'] == 0)

    for key, value in primitive:
        if not is_array(value):
            output.append("  <ITableField d={d.%s} level={level} />" % key)
        else:
            output.append("  <ITableField d={d.%s} level={level} >" % key)
            output.append("    <ITableArrayValue value={d.%s} />" % key)
            output.append("  </ITableField>")

    # complex values will be rendered as indented components
    for key, value in complex:
        component_name, generate, add_field = jinja_component_name(prefix, value)
        if not component_name:
            continue
        if generate:
            generate_jinjax_component(value if not is_array(value) else value['child'],
                                      target_dir, component_name, prefix)
        if value['detail'] == 'array':
            output.append("  {%% for it in array(d.%s) %%}" % key)
            if add_field:
                output.append("    <ITableField d={it} level={level} >")
                output.append("      <%s d={it} level={level+1} />" % component_name)
                output.append("    </ITableField>")
            else:
                output.append("    <%s d={it} level={level+1} />" % component_name)
            output.append("  {% endfor %}")
        else:
            if add_field:
                output.append("  <ITableField d={md.%s} >" % key)
                output.append("    <%s d={d.%s} level={level+1} />" % (component_name, key))
                output.append("  </ITableField>")
            else:
                output.append("  <%s d={d.%s} level={level+1} />" % (component_name, key))

    output.append("</ITableSection>")

    (target_dir / f'{name}.jinja').write_text('\n'.join(output))


def is_array(data):
    return 'child' in data


def jinja_component_name(prefix, data):
    """
    returns component, generate, add_field
    """
    detail = data['detail']

    if detail is False:
        return None, False, False

    if detail == 'taxonomy_item':
        return 'ITaxonomyItem', False, True

    if detail == 'vocabulary_item':
        return 'IVocabularyItem', False, True

    if detail == "array":
        data = data['child']
        return jinja_component_name(prefix, data)

    return prefix + ''.join([x.capitalize() for x in detail.split('_')]), True, False


def add_depth(data):
    data['depth'] = 0
    if 'children' in data:
        for key, value in data['children'].items():
            add_depth(value)
            data['depth'] = max(data['depth'], value['depth'] + 1)
    if 'child' in data:
        add_depth(data['child'])
        data['depth'] = max(data['depth'], data['child']['depth'])


if __name__ == '__main__':
    import click
    @click.command()
    @click.argument('ui_file')
    @click.argument('output_dir')
    @click.argument('prefix')
    def main(ui_file, output_dir, prefix):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        create_detail_page(ui_file, output_dir, prefix)

    main()