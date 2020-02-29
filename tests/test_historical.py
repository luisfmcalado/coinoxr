from coinoxr import Historical
from coinoxr.requestor import Requestor
from coinoxr.response import Response
from tests.fixtures import content


class TestHistorical:
    def test_get_historical(self, requestor):
        result = Historical(requestor).get("2012-07-10")
        assert isinstance(result, Response)
        assert result.code == 200
        assert result.body == self.historical()

    def test_get_historical_with_oxr_defaults(self, client):
        import coinoxr

        coinoxr.app_id = "fake_app_id"
        coinoxr.default_http_client = client

        result = Historical().get("2012-07-10")
        assert isinstance(result, Response)
        assert result.code == 200
        assert result.body == self.historical()

    def test_get_historical_is_called_with_defaults(self, mocker, client_get_mock):
        client = client_get_mock(200, self.historical())
        requestor = Requestor("fake_app_id", client)
        Historical(requestor).get("2012-07-10")

        client.get.assert_called_with(self.url(), params=self.params())

    def test_get_historical_with_pretty_print(self, mocker, client_get_mock):
        client = client_get_mock(200, self.historical())
        requestor = Requestor("fake_app_id", client)
        Historical(requestor).get("2012-07-10", pretty_print=True)

        client.get.assert_called_with(
            self.url(), params={**self.params(), "prettyprint": True},
        )

    def test_get_historical_with_base(self, mocker, client_get_mock):
        client = client_get_mock(200, self.historical())
        requestor = Requestor("fake_app_id", client)
        Historical(requestor).get("2012-07-10", base="EUR")

        client.get.assert_called_with(
            self.url(), params={**self.params(), "base": "EUR"},
        )

    def test_get_historical_with_symbols(self, mocker, client_get_mock):
        client = client_get_mock(200, self.historical())
        requestor = Requestor("fake_app_id", client)
        Historical(requestor).get("2012-07-10", symbols="USD,EUR")

        client.get.assert_called_with(
            self.url(), params={**self.params(), "symbols": "USD,EUR"},
        )

    def test_get_historical_with_alternative(self, mocker, client_get_mock):
        client = client_get_mock(200, self.historical())
        requestor = Requestor("fake_app_id", client)
        Historical(requestor).get("2012-07-10", show_alternative=True)

        client.get.assert_called_with(
            self.url(), params={**self.params(), "show_alternative": True},
        )

    def test_get_historical_returns_invalid_app_id(self, client):
        result = Historical(Requestor("0", client)).get("2012-07-10", base="USD")
        assert isinstance(result, Response)
        assert result.code == 401
        assert result.body == content("tests/fixtures/invalid_app_id.json")

    def test_get_historical_returns_missing_app_id(self, client):
        result = Historical(Requestor("missing_app_id", client)).get("2012-07-10")
        assert isinstance(result, Response)
        assert result.code == 401
        assert result.body == content("tests/fixtures/missing_app_id.json")

    def test_get_historical_returns_invalid_date(self, requestor):
        result = Historical(requestor).get("2013-07-100")
        assert isinstance(result, Response)
        assert result.code == 400
        assert result.body == content("tests/fixtures/invalid_date.json")

    def test_get_historical_returns_missing_date(self, requestor):
        result = Historical(requestor).get("2012-07-11")
        assert isinstance(result, Response)
        assert result.code == 400
        assert result.body == content("tests/fixtures/date_not_available.json")

    def historical(self):
        return content("tests/fixtures/2012-07-10.json")

    def url(self):
        return "https://openexchangerates.org/api/historical/2012-07-10.json"

    def params(self):
        return {
            "prettyprint": False,
            "app_id": "fake_app_id",
            "show_alternative": False,
        }
