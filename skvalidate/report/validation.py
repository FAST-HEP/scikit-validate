import os
from .. import __skvalidate_root__

from .. import compare
def produce_validation_report(stages, jobs, validation_json, **kwargs):
    # 1. for job in jobs: get the validation_json
    pass


def create_detailed_report(data, output_dir='.', output_file='validation_report_detail.html'):
    """Create detailed report (with plots)"""
    template = os.path.join(__skvalidate_root__, 'data', 'templates', 'report', 'validation_detail.md')
    return os.path.join(output_dir, output_file)


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
            distributions=distributions.keys()
        )
    return summary
