import os

from jinja2 import Template
import markdown2
import pdfkit

from .. import __skvalidate_root__

from .. import compare
from .. import gitlab


def produce_validation_report(stages, jobs, validation_json, **kwargs):
    """Produce validation report inside CI pipeline.

    @param stages: the GitLab CI stages to consider
    @param jobs: the job names to consider
    @param validation_json: local job path to validation JSON output

    @return summary of validation findings with pointers to details
    """
    download_json = dict(validation_json=validation_json)
    jobs = gitlab.get_jobs_for_stages(stages, download_json=download_json, job_filter=jobs)
    data = {}
    for name, job in jobs.items():
        outputs = download_validation_outputs(job)
        outputs = update_image_urls(outputs)
        data[name] = job['validation_json'][name]
        data[name]['distributions'].update(outputs)
        validation_output_file = 'validation_report_{0}.html'.format(name)
        details = create_detailed_report(data[name], output_dir='.', output_file=validation_output_file)
        data[name]['web_url_to_details'] = details
    summary = create_summary(data)
    return summary


def download_validation_outputs(job):
    """Download validation specific outputs.

    @param job: single GitLab CI job as produced by gitlab.get_jobs_for_stages

    @return dictionary of job distribution names and image paths
    """
    name = job['name']
    data = job['validation_json'][name]
    base_output_dir = os.path.join(data['output_path'], name)
    if not os.path.exists(base_output_dir):
        os.makedirs(base_output_dir)

    distributions = data['distributions']
    results = {}
    for d_name, info in distributions.items():
        if 'image' not in info:
            continue
        image = info['image']
        output_file = image.replace(data['output_path'], base_output_dir)
        gitlab.download_artifact(job['id'], image, output_file=output_file)
        results[d_name] = {'image': output_file}
    return results


def update_image_urls(outputs):
    """Update image URLs for this CI job

    @param outputs: dictionary of {'name': {'image':path}}

    @return aritfact path with RAW url for each image path
    """
    results = {}
    job_id = os.environ.get('CI_JOB_ID')
    for name, info in outputs.items():
        image_path = info['image']
        path = gitlab.path_and_job_id_to_artifact_url(image_path, job_id, 'raw')
        results[name] = dict(image=path)
    return results


def create_detailed_report(data, output_dir='.', output_file='validation_report_detail.html'):
    """Create detailed (HTML) report (with plots)

    @param data: the validation data
    @param output_dir: the output directory for the report. Default: .
    @param output_file: name of output file (HTML format)

    @return: link to produced validation report
    """
    template = os.path.join(__skvalidate_root__, 'data', 'templates', 'report', 'default', 'validation_detail.md')
    with open(template) as f:
        content = f.read()
    content = _add_table_of_contents(content, data)

    full_path = os.path.join(os.path.abspath(output_dir), output_file)
    with open(full_path, 'w') as f:
        f.write(content)
    pdfkit.from_file(full_path, full_path + '.pdf')
    local = 'CI' not in os.environ
    if local:
        protocol = 'file://'
        link = protocol + os.path.join(os.path.abspath(output_dir), output_file)
    else:
        path = os.path.join(output_dir, output_file)
        job_id = os.environ.get('CI_JOB_ID')
        link = gitlab.path_and_job_id_to_artifact_url(path, job_id, 'raw')
    return link


def create_summary(data):
    """Create validation summary.

    @param data: validation data

    @return: markdown content of validation summary
    """
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
    """Add table of contents to template

    @param content: markdown template content
    @param data: data to fill the template

    @return HTML version of HTML content
    """
    # render once to get the structure
    template = Template(content)
    data['table_of_contents'] = ''
    tmp = template.render(**data)
    # create table of contents
    tmp = markdown2.markdown(tmp, extras=["toc"])
    table_of_contents = tmp.toc_html

    # render with table of contents
    template = Template(content)
    data['table_of_contents'] = table_of_contents
    tmp = template.render(**data)

    return markdown2.markdown(tmp)
