from coinoxr import Convert
from coinoxr.requestor import Requestor
from coinoxr.response import Response
from tests.fixtures import content


class TestConvert:
    def test_get_convert(self, requestor):
        result = Convert(requestor).get(10, "USD", "EUR")
        assert isinstance(result, Response)
        assert result.code == 200
        assert result.body == self.convert()

    def test_get_convert_with_oxr_defaults(self, client):
        import coinoxr

        coinoxr.app_id = "fake_app_id"
        coinoxr.default_http_client = client

        result = Convert().get(10, "USD", "EUR")
        assert isinstance(result, Response)
        assert result.code == 200
        assert result.body == self.convert()

    def test_get_convert_is_called_with_defaults(self, mocker, client_get_mock):
        client = client_get_mock(200, self.convert())
        requestor = Requestor("fake_app_id", client)
        Convert(requestor).get(10, "USD", "EUR")

        client.get.assert_called_with(self.url(), params=self.params())

    def test_get_convert_with_pretty_print(self, mocker, client_get_mock):
        client = client_get_mock(200, self.convert())
        requestor = Requestor("fake_app_id", client)
        Convert(requestor).get(10, "USD", "EUR", pretty_print=True)

        client.get.assert_called_with(
            self.url(), params={**self.params(), "prettyprint": True},
        )

    def test_get_convert_returns_invalid_app_id(self, client):
        result = Convert(Requestor("0", client)).get(10, "USD", "EUR")
        assert isinstance(result, Response)
        assert result.code == 401
        assert result.body == content("tests/fixtures/invalid_app_id.json")

    def test_get_convert_returns_missing_app_id(self, client):
        result = Convert(Requestor("missing_app_id", client)).get(10, "USD", "EUR")
        assert isinstance(result, Response)
        assert result.code == 401
        assert result.body == content("tests/fixtures/missing_app_id.json")

    def test_get_convert_returns_invalid_amount(self, requestor):
        result = Convert(requestor).get(-1, "USD", "EUR")
        assert isinstance(result, Response)
        assert result.code == 400
        assert result.body == content("tests/fixtures/invalid_amount.json")

    def test_get_convert_returns_invalid_currency(self, requestor):
        result = Convert(requestor).get(10, "US", "EUR")
        assert isinstance(result, Response)
        assert result.code == 400
        assert result.body == content("tests/fixtures/invalid_currency.json")

    def convert(self):
        return content("tests/fixtures/convert.json")

    def url(self):
        return "https://openexchangerates.org/api/convert/10/USD/EUR"

    def params(self):
        return {
            "prettyprint": False,
            "app_id": "fake_app_id",
        }
