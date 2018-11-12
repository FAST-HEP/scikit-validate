import pytest
from skvalidate.commands.get_target_branch import _pick_target_branch


@pytest.mark.parametrize('target_branch,target_branches,default_branch,ci_commit_ref_name,expected', [
    (
        'test',
        ['A', 'B', 'C'],
        'Z',
        'feature',
        'test'
    ),
    (
        None,
        ['A', 'B', 'C'],
        'Z',
        'feature',
        'Z'
    ),
    (
        None,
        ['A', 'B', 'C'],
        'C',
        'A',
        'A'
    ),
    (
        None,
        ['A', 'B', 'C'],
        None,
        'B',
        'B'
    )
])
def test_pick_target_branch(target_branch, target_branches, default_branch, ci_commit_ref_name, expected):
    picked_branch = _pick_target_branch(target_branch, target_branches, default_branch, ci_commit_ref_name)
    assert picked_branch == expected
