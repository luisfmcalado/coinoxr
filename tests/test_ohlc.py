from coinoxr import Ohlc
from coinoxr.requestor import Requestor
from coinoxr.response import Response
from tests.fixtures import content


class TestHistorical:
    def test_get_ohlc(self, requestor):
        result = Ohlc(requestor).get("2017-07-17T11:00:00Z", "30m")
        assert isinstance(result, Response)
        assert result.code == 200
        assert result.body == self.historical()

    def test_get_ohlc_with_oxr_defaults(self, client):
        import coinoxr

        coinoxr.app_id = "fake_app_id"
        coinoxr.default_http_client = client

        result = Ohlc().get("2017-07-17T11:00:00Z", "30m")
        assert isinstance(result, Response)
        assert result.code == 200
        assert result.body == self.historical()

    def test_get_ohlc_is_called_with_defaults(self, mocker, client_get_mock):
        client = client_get_mock(200, self.historical())
        requestor = Requestor("fake_app_id", client)
        Ohlc(requestor).get("2017-07-17T11:00:00Z", "30m")

        client.get.assert_called_with(self.url(), params=self.params())

    def test_get_ohlc_with_pretty_print(self, mocker, client_get_mock):
        client = client_get_mock(200, self.historical())
        requestor = Requestor("fake_app_id", client)
        Ohlc(requestor).get("2017-07-17T11:00:00Z", "30m", pretty_print=True)

        client.get.assert_called_with(
            self.url(), params={**self.params(), "prettyprint": True},
        )

    def test_get_ohlc_with_base(self, mocker, client_get_mock):
        client = client_get_mock(200, self.historical())
        requestor = Requestor("fake_app_id", client)
        Ohlc(requestor).get("2017-07-17T11:00:00Z", "30m", base="EUR")

        client.get.assert_called_with(
            self.url(), params={**self.params(), "base": "EUR"},
        )

    def test_get_ohlc_with_symbols(self, mocker, client_get_mock):
        client = client_get_mock(200, self.historical())
        requestor = Requestor("fake_app_id", client)
        Ohlc(requestor).get("2017-07-17T11:00:00Z", "30m", symbols="USD,EUR")

        client.get.assert_called_with(
            self.url(), params={**self.params(), "symbols": "USD,EUR"},
        )

    def test_get_ohlc_returns_invalid_app_id(self, client):
        result = Ohlc(Requestor("0", client)).get(
            "2017-07-17T11:00:00Z", "30m", base="USD"
        )
        assert isinstance(result, Response)
        assert result.code == 401
        assert result.body == content("tests/fixtures/invalid_app_id.json")

    def test_get_ohlc_returns_missing_app_id(self, client):
        result = Ohlc(Requestor("missing_app_id", client)).get(
            "2017-07-17T11:00:00Z", "30m"
        )
        assert isinstance(result, Response)
        assert result.code == 401
        assert result.body == content("tests/fixtures/missing_app_id.json")

    def test_get_ohlc_returns_invalid_date(self, requestor):
        result = Ohlc(requestor).get("2017-07-17T11:00:00Z", "100m")
        assert isinstance(result, Response)
        assert result.code == 400
        assert result.body == content("tests/fixtures/invalid_period_start_point.json")

    def test_get_ohlc_returns_invalid_start_time(self, requestor):
        result = Ohlc(requestor).get("11:00:00", "30m")
        assert isinstance(result, Response)
        assert result.code == 400
        assert result.body == content("tests/fixtures/invalid_start_time.json")

    def historical(self):
        return content("tests/fixtures/ohlc.json")

    def url(self):
        return "https://openexchangerates.org/api/ohlc.json"

    def params(self):
        return {
            "prettyprint": False,
            "app_id": "fake_app_id",
            "start_time": "2017-07-17T11:00:00Z",
            "period": "30m",
        }
