from unittest.mock import patch

import skvalidate.gitlab as gl


def test_connect(gitlab_settings):
    with patch.dict("os.environ", gitlab_settings.to_dict()):
        assert gl.GITLAB_CONNECTION is None
        gl._connect()
        assert gl.GITLAB_CONNECTION is not None


def test_get_merge_request(gitlab_settings):
    with patch.dict("os.environ", gitlab_settings.to_dict()):
        mr = gl._get_merge_request()
        assert mr is not None
        assert mr.iid == 1


def test_get_merge_request_without_id(gitlab_settings):
    del gitlab_settings.CI_MERGE_REQUEST_IID
    with patch.dict("os.environ", gitlab_settings.to_dict()):
        mr = gl._get_merge_request()
        assert mr is not None
        assert mr.iid == 1
