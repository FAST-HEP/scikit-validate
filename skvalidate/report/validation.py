import os

from jinja2 import Template
import markdown2

from .. import __skvalidate_root__

from .. import compare


def produce_validation_report(stages, jobs, validation_json, **kwargs):
    # 1. for job in jobs: get the validation_json
    pass


def create_detailed_report(data, output_dir='.', output_file='validation_report_detail.html'):
    """Create detailed report (with plots)"""
    template = os.path.join(__skvalidate_root__, 'data', 'templates', 'report', 'default', 'validation_detail.md')
    with open(template) as f:
        content = f.read()
    content = _add_table_of_contents(content, data)

    full_path = os.path.join(os.path.abspath(output_dir), output_file)
    with open(full_path, 'w') as f:
        f.write(content)
    # if not in CI --> localhost link
    local = True
    protocol = 'file://'
    link = protocol + os.path.join(os.path.abspath(output_dir), output_file)
    if not local:
        pass
    return link


def create_summary(data):
    """Create validation summary."""
    summary = {}
    for name, info in data.items():
        distributions = info['root_diff']['distributions']
        status = compare.SUCCESS

        failed = info['root_diff'][compare.FAILED]
        error = info['root_diff'][compare.ERROR]
        unknown = info['root_diff'][compare.UNKNOWN]
        n_bad = len(failed) + len(error)

        if n_bad > 0:
            status = compare.FAILED
        summary[name] = dict(
            status=status,
            differ=failed,
            unknown=unknown,
            error=error,
            distributions=distributions.keys(),
            web_url_to_details=info['web_url_to_details'],
        )
    return summary


def _add_table_of_contents(content, data):
    template = Template(content)
    data['table_of_contents'] = ''
    tmp = template.render(**data)
    tmp = markdown2.markdown(tmp, extras=["toc"])
    table_of_contents = tmp.toc_html

    template = Template(content)
    data['table_of_contents'] = table_of_contents
    tmp = template.render(**data)
    return markdown2.markdown(tmp)
