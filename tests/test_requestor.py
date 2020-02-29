import pytest

from coinoxr.requestor import Requestor
from coinoxr.response import Response
from tests.stub_client import StubHttpClient
from coinoxr.error import AppIdError


class TestRequestor:
    @pytest.fixture
    def http_client(self, mocker):
        return mocker.Mock(StubHttpClient)

    @pytest.fixture
    def requestor(self, http_client):
        return Requestor("fake_api_key", client=http_client)

    @pytest.fixture
    def mock_response(self, http_client, mocker):
        def mock_response(status_code, body):
            http_client.get = mocker.MagicMock(return_value=Response(status_code, body))

        return mock_response

    @pytest.fixture
    def mock_bad_response(self, http_client, mocker):
        def mock_bad_response(status_code):
            http_client.get = mocker.MagicMock(return_value=Response(status_code, None))

        return mock_bad_response

    def test_get_invalid_method(self, requestor, mock_bad_response):
        mock_bad_response(405)
        result = requestor.get("", {})
        assert result.code == 405
        assert result.body is None

    def test_get_result(self, requestor, mock_response):
        data = {"base": "USD"}
        mock_response(200, data)
        result = requestor.get("usage", {})
        assert result.code == 200
        assert result.body == data

    def test_missing_api_id_exception(self, http_client):
        import coinoxr

        coinoxr.app_id = None
        message = "No API key provided. Setup coinoxr.app_id = <API-Key> or app_id argument.You can get the API key from open exchange rates dashboard."
        with pytest.raises(AppIdError) as ex:
            Requestor(None, client=http_client)
        assert message in str(ex.value)

    def test_skip_app_id(self, http_client, mock_response):
        data = {"base": "USD"}
        mock_response(200, data)
        requestor = Requestor(None, client=http_client, skip_app_id=True)
        result = requestor.get("usage", {})

        assert result.code == 200
        assert result.body == data
