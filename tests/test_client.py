import pytest

from coinoxr.client import RequestsClient
from coinoxr.response import Response


class TestRequestsClient:
    @pytest.fixture
    def requests_mock(self, mocker):
        def requests_mock(response):
            return mocker.patch("requests.get", return_value=response, autospec=True,)

        return requests_mock

    @pytest.fixture
    def response_mock(self, mocker, requests_mock):
        def response_mock(status_code, body):
            response_mock = mocker.Mock()
            response_mock.json = mocker.Mock(return_value=body)
            response_mock.status_code = status_code
            return requests_mock(response_mock)

        return response_mock

    def test_get_request_with_params(self, mocker, response_mock):
        body = {"field2": "value1"}
        status = 200
        requests = response_mock(status, body)

        url = "http://fake.url"
        params = {"field1": 1000}
        RequestsClient().get(url, params)

        requests.assert_called_with(url, params)

    def test_get_request_returns_response(self, mocker, response_mock):
        body = {"field2": "value1"}
        status = 200
        response_mock(status, body)

        response = RequestsClient().get("http://fake.url", {"field1": 1000})

        assert isinstance(response, Response)
        assert response.code == status
        assert response.body == body

    def test_get_request_returns_no_body(self, mocker, requests_mock):
        status_code = 400
        response_mock = mocker.Mock()
        response_mock.json = mocker.Mock(
            side_effect=ValueError("No JSON object could be decoded")
        )
        response_mock.status_code = status_code
        requests_mock(response_mock)

        response = RequestsClient().get("http://fake.url", {"field1": 1000})

        assert isinstance(response, Response)
        assert response.code == status_code
        assert response.body is None
