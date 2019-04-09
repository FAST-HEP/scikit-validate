import os
import pytest

from skvalidate.report.validation import _get_links_for_reports


@pytest.mark.parametrize('output_files,ci,expected_links', [
    (
        dict(pdf='report.pdf'),
        True,
        dict(pdf='https://gitlab.example.com/group/MyProject/-/jobs/42/artifacts/file/report.pdf'),
    ),
    (
        dict(pdf='report.pdf', md=os.getcwd() + '/output/report.md', html=os.getcwd() + '/output/report.html'),
        True,
        dict(
            pdf='https://gitlab.example.com/group/MyProject/-/jobs/42/artifacts/file/report.pdf',
            md='https://gitlab.example.com/group/MyProject/-/jobs/42/artifacts/file/output/report.md',
            html='https://gitlab.example.com/group/MyProject/-/jobs/42/artifacts/raw/output/report.html',
        ),
    ),
    (
        dict(pdf='report.pdf', md=os.getcwd() + '/output/report.md', html=os.getcwd() + '/output/report.html'),
        False,
        dict(
            pdf='file://' + os.getcwd() + '/report.pdf',
            md='file://' + os.getcwd() + '/output/report.md',
            html='file://' + os.getcwd() + '/output/report.html',
        ),
    ),
])
def test_get_links_for_reports(output_files, ci, expected_links):
    if ci:
        os.environ['CI'] = str(ci)
        os.environ['CI_JOB_ID'] = '42'
        os.environ['CI_PROJECT_URL'] = 'https://gitlab.example.com/group/MyProject'
    else:
        if 'CI' in os.environ:
            del os.environ['CI']
    links = _get_links_for_reports(output_files)
    assert links == expected_links
