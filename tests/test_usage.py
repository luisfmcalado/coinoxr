from coinoxr import Usage
from coinoxr.requestor import Requestor
from coinoxr.response import Response
from tests.fixtures import content


class TestUsage:
    def test_get_usage(self, requestor):
        result = Usage(requestor).get()
        assert isinstance(result, Response)
        assert result.code == 200
        assert result.body == self.usage()

    def test_get_usage_with_oxr_defaults(self, client):
        import coinoxr

        coinoxr.app_id = "fake_app_id"
        coinoxr.default_http_client = client

        result = Usage().get()
        assert isinstance(result, Response)
        assert result.code == 200
        assert result.body == self.usage()

    def test_get_usage_called_with_defaults(self, client_get_mock):
        client = client_get_mock(200, self.usage())
        requestor = Requestor("fake_app_id", client)
        Usage(requestor).get()

        client.get.assert_called_with(
            self.url(), params=self.params(),
        )

    def test_get_usage_with_pretty_print(self, client_get_mock):
        client = client_get_mock(200, self.usage())
        requestor = Requestor("fake_app_id", client)
        Usage(requestor).get(pretty_print=True)

        client.get.assert_called_with(
            self.url(), params={**self.params(), "prettyprint": True},
        )

    def test_get_usage_returns_invalid_app_id(self, client):
        result = Usage(Requestor("0", client)).get()
        assert isinstance(result, Response)
        assert result.code == 401
        assert result.body == content("tests/fixtures/invalid_app_id.json")

    def test_get_usage_returns_missing_app_id(self, client):
        result = Usage(Requestor("missing_app_id", client)).get()
        assert isinstance(result, Response)
        assert result.code == 401
        assert result.body == content("tests/fixtures/missing_app_id.json")

    def usage(self):
        return content("tests/fixtures/usage.json")

    def url(self):
        return "https://openexchangerates.org/api/usage.json"

    def params(self):
        return {
            "prettyprint": False,
            "app_id": "fake_app_id",
        }
