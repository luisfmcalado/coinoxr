from coinoxr import TimeSeries
from coinoxr.requestor import Requestor
from coinoxr.response import Response
from tests.fixtures import content


class TestTimeSeries:
    def test_get_timeseries(self, requestor):
        result = TimeSeries(requestor).get("2012-07-10", "2012-07-12")
        assert isinstance(result, Response)
        assert result.code == 200
        assert result.body == self.series()

    def test_get_timeseries_with_oxr_defaults(self, client):
        import coinoxr

        coinoxr.app_id = "fake_app_id"
        coinoxr.default_http_client = client

        result = TimeSeries().get("2012-07-10", "2012-07-12")
        assert isinstance(result, Response)
        assert result.code == 200
        assert result.body == self.series()

    def test_get_timeseries_is_called_with_defaults(self, mocker, client_get_mock):
        client = client_get_mock(200, self.series())
        requestor = Requestor("fake_app_id", client)
        TimeSeries(requestor).get("2012-07-10", "2012-07-12")

        client.get.assert_called_with(self.url(), params=self.params())

    def test_get_timeseries_with_pretty_print(self, mocker, client_get_mock):
        client = client_get_mock(200, self.series())
        requestor = Requestor("fake_app_id", client)
        TimeSeries(requestor).get("2012-07-10", "2012-07-12", pretty_print=True)

        client.get.assert_called_with(
            self.url(), params={**self.params(), "prettyprint": True},
        )

    def test_get_timeseries_with_base(self, mocker, client_get_mock):
        client = client_get_mock(200, self.series())
        requestor = Requestor("fake_app_id", client)
        TimeSeries(requestor).get("2012-07-10", "2012-07-12", base="EUR")

        client.get.assert_called_with(
            self.url(), params={**self.params(), "base": "EUR"},
        )

    def test_get_timeseries_with_symbols(self, mocker, client_get_mock):
        client = client_get_mock(200, self.series())
        requestor = Requestor("fake_app_id", client)
        TimeSeries(requestor).get("2012-07-10", "2012-07-12", symbols="USD,EUR")

        client.get.assert_called_with(
            self.url(), params={**self.params(), "symbols": "USD,EUR"},
        )

    def test_get_timeseries_with_alternative(self, mocker, client_get_mock):
        client = client_get_mock(200, self.series())
        requestor = Requestor("fake_app_id", client)
        TimeSeries(requestor).get("2012-07-10", "2012-07-12", show_alternative=True)

        client.get.assert_called_with(
            self.url(), params={**self.params(), "show_alternative": True},
        )

    def test_get_timeseries_returns_invalid_app_id(self, client):
        result = TimeSeries(Requestor("0", client)).get(
            "2012-07-10", "2012-07-12", base="USD"
        )
        assert isinstance(result, Response)
        assert result.code == 401
        assert result.body == content("tests/fixtures/invalid_app_id.json")

    def test_get_timeseries_returns_missing_app_id(self, client):
        result = TimeSeries(Requestor("missing_app_id", client)).get(
            "2012-07-10", "2012-07-12"
        )
        assert isinstance(result, Response)
        assert result.code == 401
        assert result.body == content("tests/fixtures/missing_app_id.json")

    def test_get_timeseries_returns_invalid_date(self, requestor):
        result = TimeSeries(requestor).get("2013-07-100", "2012-07-12")
        assert isinstance(result, Response)
        assert result.code == 400
        assert result.body == content("tests/fixtures/invalid_date_range.json")

    def test_get_timeseries_returns_missing_date(self, requestor):
        result = TimeSeries(requestor).get("2020-07-11", "2020-07-12")
        assert isinstance(result, Response)
        assert result.code == 400
        assert result.body == content("tests/fixtures/range_not_available.json")

    def series(self):
        return content("tests/fixtures/time-series.json")

    def url(self):
        return "https://openexchangerates.org/api/time-series.json"

    def params(self):
        return {
            "prettyprint": False,
            "app_id": "fake_app_id",
            "show_alternative": False,
            "start": "2012-07-10",
            "end": "2012-07-12",
        }
