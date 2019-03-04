import os

from jinja2 import Template
import markdown2
from xhtml2pdf import pisa

from .. import __skvalidate_root__

from .. import compare
from .. import gitlab
from .. import logger


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
        # write out .md with full paths, HTML with local paths and PDF with local paths
        data[name] = job['validation_json'][name]
        data[name]['job_name'] = name
        validation_output_file = 'validation_report_{0}'.format(name)

        details = create_detailed_report(
            data[name], output_dir='.',
            output_file=validation_output_file,
            formats=['pdf']
        )

        # data[name]['distributions'].update(outputs)
        for d, info in data[name]['distributions'].items():
            if 'image' in info:
                info['image'] = outputs[d]['image']
        details = create_detailed_report(
            data[name], output_dir='.',
            output_file=validation_output_file,
            formats=['md', 'html']
        )
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
        logger.debug('Creating local path {0}'.format(base_output_dir))
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
    if 'CI' not in os.environ:
        return outputs
    results = {}
    job_id = os.environ.get('CI_JOB_ID')
    for name, info in outputs.items():
        image_path = info['image']
        path = gitlab.path_and_job_id_to_artifact_url(image_path, job_id, 'raw')
        results[name] = dict(image=path)
    return results


def create_detailed_report(data, output_dir='.', output_file='validation_report_detail.html', formats=['md']):
    """Create detailed (HTML) report (with plots)

    @param data: the validation data
    @param output_dir: the output directory for the report. Default: .
    @param output_file: name of output file (HTML format)

    @return: link to produced validation report
    """
    template_path = os.path.join(__skvalidate_root__, 'data', 'templates', 'report', 'default', 'validation_detail.md')
    full_path = os.path.join(os.path.abspath(output_dir), output_file)

    if 'md' in formats:
        md_output_file = full_path + '.md'
        _create_detailed_report_md(_read_template(template_path), data, md_output_file)
    if 'html' in formats or 'pdf' in formats:
        html_output_file = full_path + '.html'
        _create_detailed_report_html(template_path, data, html_output_file)
        if 'pdf' in formats:
            pdf_output_file = full_path + '.pdf'
            _create_pdf(html_output_file, pdf_output_file)

    local = 'CI' not in os.environ
    if local:
        protocol = 'file://'
        link = protocol + os.path.join(os.path.abspath(output_dir), output_file)
    else:
        job_id = os.environ.get('CI_JOB_ID')
        path_type = 'file'
        if 'pdf' in formats:
            path = os.path.join(output_dir, pdf_output_file)
            link = gitlab.path_and_job_id_to_artifact_url(path, job_id)
        elif 'html' in formats:
            path = os.path.join(output_dir, html_output_file)
            path_type = 'raw'
        else:
            path = os.path.join(output_dir, md_output_file)
        link = gitlab.path_and_job_id_to_artifact_url(path, job_id, path_type)
    return link


def _create_detailed_report_md(template, data, output_file):
    data['table_of_contents'] = ''
    content = template.render(**data)
    with open(output_file, 'w') as f:
        f.write(content)


def _read_template(template_path):
    with open(template_path) as f:
        content = f.read()
    return Template(content)


def _create_pdf(input_file, output_file):
    with open(output_file, 'wb') as o:
        with open(input_file) as f:
            pisa.pisaDocument(f.read(), dest=o)


def _create_detailed_report_html(template_path, data, output_file):
    """Add table of contents to template

    @param template_path: path to template
    @param data: data to fill the template
    @param

    @return HTML version of HTML content
    """
    template = _read_template(template_path)
    # render once to get the structure
    data['table_of_contents'] = ''
    tmp = template.render(**data)
    # create table of contents
    tmp = markdown2.markdown(tmp, extras=["toc"])
    table_of_contents = tmp.toc_html

    # render with table of contents
    template = _read_template(template_path)
    data['table_of_contents'] = table_of_contents
    tmp = template.render(**data)

    content = markdown2.markdown(tmp)
    with open(output_file, 'w') as f:
        f.write(content)


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
