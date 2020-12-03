import gitlab
import pytest
import responses

project_content = {"name": "name", "id": 1}

@pytest.fixture
def gl():
    return gitlab.Gitlab(
        "http://localhost",
        private_token="private_token",
        ssl_verify=True,
        api_version=4,
    )

@pytest.fixture
def resp_get_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1",
            json=project_content,
            content_type="application/json",
            status=200,
        )
        yield rsps

@pytest.fixture
def resp_list_projects():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects",
            json=[project_content],
            content_type="application/json",
            status=200,
        )
        yield rsps

@pytest.fixture
def binary_content():
    return b'{"name": "value"}'

@pytest.fixture
def resp_artifact_json(binary_content):
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1",
            json=project_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/jobs/1/artifacts/test%2Ejson",
            body=binary_content,
            content_type="application/octet-stream",
            status=200,
        )
        yield rsps

@pytest.fixture
def resp_artifact_no_such_file(binary_content):
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1",
            json=project_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/jobs/1/artifacts/test%2Ejson",
            body=binary_content,
            content_type="application/octet-stream",
            status=404,
        )
        yield rsps

@pytest.fixture
def object_file():
    import uproot
    path = 'tests/samples/objects.root'
    f = uproot.open(path)
    return f


@pytest.fixture
def scalar_type_ak_array(object_file):
    return object_file['Events']['eventID'].array()


@pytest.fixture
def object_type(object_file):
    return object_file['Events']['bees.xyPosition']


@pytest.fixture
def object_type_ak_array(object_type):
    return object_type.array()
