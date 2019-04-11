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
        # write out .md with full paths, HTML with local paths and PDF with local paths
        data[name] = job['validation_json'][name]
        data[name]['job_name'] = name
        data[name]['images'] = []
        for d, info in data[name]['distributions'].items():
            if 'image' in info:
                image = outputs[d]['image']
                logger.debug('Loading image {0} for PDF validation report'.format(image))
                data[name]['images'].append(image)
        validation_output_file = 'validation_report_{0}'.format(name)

        details = create_detailed_report(
            data[name], output_dir='.',
            output_file=validation_output_file,
            formats=['pdf']
        )

        outputs = update_image_urls(outputs)
        data[name]['images'] = []
        for d, info in data[name]['distributions'].items():
            if 'image' in info:
                image = outputs[d]['image']
                info['image'] = image
                logger.debug('Loading image {0} for HTML/MD validation report'.format(image))
                data[name]['images'].append(image)
        details.update(create_detailed_report(
            data[name], output_dir='.',
            output_file=validation_output_file,
            formats=['md', 'html']
        ))
        data[name]['web_url_to_details'] = details['pdf']
    summary = create_summary(data)
    return summary


def download_validation_outputs(job):
    """Download validation specific outputs.

    @param job: single GitLab CI job as produced by gitlab.get_jobs_for_stages

    @return dictionary of job distribution names and image paths
    """
    name = job['name']
    data = job['validation_json'][name]
    base_output_dir = data['output_path']
    if name not in base_output_dir:
        base_output_dir = os.path.join(base_output_dir, name)
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
    output_files = {}

    data['overview_batch_size'] = 8
    data['report_add_linebreaks'] = False

    if 'md' in formats:
        md_output_file = full_path + '.md'
        output_files['md'] = md_output_file
        _create_detailed_report_md(_read_template(template_path), data, md_output_file)
    if 'html' in formats or 'pdf' in formats:
        html_output_file = full_path + '.html'
        output_files['html'] = html_output_file
        _create_detailed_report_html(template_path, data, html_output_file)
    if 'pdf' in formats:
        data['overview_batch_size'] = 7
        data['report_add_linebreaks'] = True
        html_output_file = full_path + '_for_pdf.html'
        _create_detailed_report_html(template_path, data, html_output_file)
        pdf_output_file = full_path + '.pdf'
        output_files['pdf'] = pdf_output_file
        _create_pdf(html_output_file, pdf_output_file)

    links = _get_links_for_reports(output_files)
    return links


def _get_links_for_reports(output_files):
    local = 'CI' not in os.environ
    path_types = dict(md='file', pdf='file', html='raw')
    links = {}
    for format, output_file in output_files.items():
        link = ''
        if local:
            protocol = 'file://'
            link = protocol + os.path.abspath(output_file)
        else:
            job_id = os.environ.get('CI_JOB_ID')
            link = gitlab.path_and_job_id_to_artifact_url(output_file, job_id, path_types[format])
        links[format] = link
    return links


def _create_detailed_report_md(template, data, output_file):
    data['table_of_contents'] = ''
    content = template.render(**data)
    with open(output_file, 'w') as f:
        f.write(content)
    logger.debug('Created report: {0}'.format(output_file))


def _read_template(template_path):
    with open(template_path) as f:
        content = f.read()
    return Template(content)


def _create_pdf(input_file, output_file):
    with open(output_file, 'wb') as o:
        with open(input_file) as f:
            pisa.pisaDocument(f.read(), dest=o)
    logger.debug('Created report: {0}'.format(output_file))


def _create_detailed_report_html(template_path, data, output_file, table_of_contents=False):
    """Add table of contents to template

    @param template_path: path to template
    @param data: data to fill the template
    @param

    @return HTML version of HTML content
    """
    template = _read_template(template_path)
    # render once to get the structure
    data['table_of_contents'] = ''
    if table_of_contents:
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
    logger.debug('Created report: {0}'.format(output_file))


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
