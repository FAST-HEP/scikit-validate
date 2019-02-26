import os

from jinja2 import Template
import markdown2

from .. import __skvalidate_root__

from .. import compare
from .. import gitlab


def produce_validation_report(stages, jobs, validation_json, **kwargs):
    download_json = dict(validation_json=validation_json)
    jobs = gitlab.get_jobs_for_stages(stages, download_json=download_json, job_filter=jobs)
    data = {}
    for name, job in jobs.items():
        data[name] = job['validation_json'][name]
        for d_name, info in data[name]['distributions'].items():
            if 'image' in info:
                image = info['image']
                image = gitlab.path_and_job_id_to_artifact_url(image, job_id=job['id'])
                data[name]['distributions']['image'] = image
        validation_output_file = 'validation_report_{0}.html'.format(name)
        details = create_detailed_report(data[name], output_dir='.', output_file=validation_output_file)
        data[name]['web_url_to_details'] = details
    summary = create_summary(data)
    return summary


def create_detailed_report(data, output_dir='.', output_file='validation_report_detail.html'):
    """Create detailed report (with plots)"""
    template = os.path.join(__skvalidate_root__, 'data', 'templates', 'report', 'default', 'validation_detail.md')
    with open(template) as f:
        content = f.read()
    content = _add_table_of_contents(content, data)

    full_path = os.path.join(os.path.abspath(output_dir), output_file)
    with open(full_path, 'w') as f:
        f.write(content)
    local = 'CI' not in os.environ
    if local:
        protocol = 'file://'
        link = protocol + os.path.join(os.path.abspath(output_dir), output_file)
    else:
        link = gitlab.get_artifact_url(os.path.join(output_dir, output_file))
    return link


def create_summary(data):
    """Create validation summary."""
    summary = {}
    for name, info in data.items():
        distributions = info['distributions']
        status = compare.SUCCESS

        failed = info[compare.FAILED]
        error = info[compare.ERROR]
        unknown = info[compare.UNKNOWN]
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
