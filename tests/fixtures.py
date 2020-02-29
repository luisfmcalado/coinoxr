import pytest

from tests.stub_client import StubHttpClient
from coinoxr.requestor import Requestor
from coinoxr.response import Response


def content(file):
    return StubHttpClient.json(file)["content"]


@pytest.fixture
def client():
    client = StubHttpClient()
    client.add_app_id("fake_app_id")
    client.add_date("2012-07-10")
    client.add_date("2012-07-12")
    return client


@pytest.fixture
def client_get_mock(mocker):
    def client_get_mock(status_code, json):
        response = Response(status_code, json)
        client = mocker.Mock(StubHttpClient)
        client.get = mocker.Mock(return_value=response)
        return client

    return client_get_mock


@pytest.fixture
def requestor(client):
    return Requestor("fake_app_id", client)
