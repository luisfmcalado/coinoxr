from coinoxr import Latest
from coinoxr.requestor import Requestor
from coinoxr.response import Response
from tests.fixtures import content


class TestLatest:
    def test_get_latest(self, requestor):
        result = Latest(requestor).get()
        assert isinstance(result, Response)
        assert result.code == 200
        assert result.body == self.latest()

    def test_get_latest_with_oxr_defaults(self, client):
        import coinoxr

        coinoxr.app_id = "fake_app_id"
        coinoxr.default_http_client = client

        result = Latest().get()
        assert isinstance(result, Response)
        assert result.code == 200
        assert result.body == self.latest()

    def test_get_latest_is_called_with_defaults(self, mocker, client_get_mock):
        client = client_get_mock(200, self.latest())
        requestor = Requestor("fake_app_id", client)
        Latest(requestor).get()

        client.get.assert_called_with(self.url(), params=self.params())

    def test_get_latest_with_pretty_print(self, mocker, client_get_mock):
        client = client_get_mock(200, self.latest())
        requestor = Requestor("fake_app_id", client)
        Latest(requestor).get(pretty_print=True)

        client.get.assert_called_with(
            self.url(), params={**self.params(), "prettyprint": True},
        )

    def test_get_latest_with_base(self, mocker, client_get_mock):
        client = client_get_mock(200, self.latest())
        requestor = Requestor("fake_app_id", client)
        Latest(requestor).get(base="EUR")

        client.get.assert_called_with(
            self.url(), params={**self.params(), "base": "EUR"},
        )

    def test_get_latest_with_symbols(self, mocker, client_get_mock):
        client = client_get_mock(200, self.latest())
        requestor = Requestor("fake_app_id", client)
        Latest(requestor).get(symbols="USD,EUR")

        client.get.assert_called_with(
            self.url(), params={**self.params(), "symbols": "USD,EUR"},
        )

    def test_get_latest_with_alternative(self, mocker, client_get_mock):
        client = client_get_mock(200, self.latest())
        requestor = Requestor("fake_app_id", client)
        Latest(requestor).get(show_alternative=True)

        client.get.assert_called_with(
            self.url(), params={**self.params(), "show_alternative": True},
        )

    def test_get_latest_returns_invalid_app_id(self, client):
        result = Latest(Requestor("0", client)).get("USD")
        assert isinstance(result, Response)
        assert result.code == 401
        assert result.body == content("tests/fixtures/invalid_app_id.json")

    def test_get_latest_returns_missing_app_id(self, client):
        result = Latest(Requestor("missing_app_id", client)).get("USD")
        assert isinstance(result, Response)
        assert result.code == 401
        assert result.body == content("tests/fixtures/missing_app_id.json")

    def latest(self):
        return content("tests/fixtures/latest.json")

    def url(self):
        return "https://openexchangerates.org/api/latest.json"

    def params(self):
        return {
            "prettyprint": False,
            "app_id": "fake_app_id",
            "show_alternative": False,
        }
