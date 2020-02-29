from coinoxr.client import RequestsClient


default_http_client = RequestsClient()
default_url = "https://openexchangerates.org/api/"
app_id = None


def base_url(path):
    return default_url + path


from coinoxr.usage import Usage  # noqa
from coinoxr.latest import Latest  # noqa
from coinoxr.historical import Historical  # noqa
from coinoxr.currency import Currency  # noqa
from coinoxr.time_series import TimeSeries  # noqa
from coinoxr.convert import Convert  # noqa
from coinoxr.ohlc import Ohlc  # noqa
