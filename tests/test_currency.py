from coinoxr import Currency
from coinoxr.requestor import Requestor
from coinoxr.response import Response
from tests.fixtures import content


class TestCurrency:
    def test_get_currencies(self, requestor):
        result = Currency(requestor).get()
        assert isinstance(result, Response)
        assert result.code == 200
        assert result.body == self.currencies()

    def test_get_currencies_with_oxr_defaults(self, client):
        import coinoxr

        coinoxr.app_id = "fake_app_id"
        coinoxr.default_http_client = client

        result = Currency().get()
        assert isinstance(result, Response)
        assert result.code == 200
        assert result.body == self.currencies()

    def test_get_currencies_is_called_with_defaults(self, mocker, client_get_mock):
        client = client_get_mock(200, self.currencies())
        requestor = Requestor("fake_app_id", client, skip_app_id=True)
        Currency(requestor).get()

        client.get.assert_called_with(self.url(), params=self.params())

    def test_get_currencies_with_pretty_print(self, mocker, client_get_mock):
        client = client_get_mock(200, self.currencies())
        requestor = Requestor("fake_app_id", client, skip_app_id=True)
        Currency(requestor).get(pretty_print=True)

        client.get.assert_called_with(
            self.url(), params={**self.params(), "prettyprint": True},
        )

    def test_get_currencies_with_alternative(self, mocker, client_get_mock):
        client = client_get_mock(200, self.currencies())
        requestor = Requestor("fake_app_id", client, skip_app_id=True)
        Currency(requestor).get(show_alternative=True)

        client.get.assert_called_with(
            self.url(), params={**self.params(), "show_alternative": True},
        )

    def test_get_currencies_with_inactive(self, mocker, client_get_mock):
        client = client_get_mock(200, self.currencies())
        requestor = Requestor("fake_app_id", client, skip_app_id=True)
        Currency(requestor).get(show_inactive=True)

        client.get.assert_called_with(
            self.url(), params={**self.params(), "show_inactive": True},
        )

    def currencies(self):
        return content("tests/fixtures/currencies.json")

    def url(self):
        return "https://openexchangerates.org/api/currencies.json"

    def params(self):
        return {
            "prettyprint": False,
            "show_alternative": False,
            "show_inactive": False,
        }
