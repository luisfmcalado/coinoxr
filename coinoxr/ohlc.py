from coinoxr.requestor import Requestor


class Ohlc:
    def __init__(self, requestor=None):
        self._requestor = requestor
        if requestor is None:
            self._requestor = Requestor()

    def get(
        self, start_time, period, base=None, pretty_print=False, symbols=None,
    ):
        params = {
            "prettyprint": pretty_print,
            "period": period,
            "start_time": start_time,
        }

        if base is not None:
            params["base"] = base

        if symbols is not None:
            params["symbols"] = symbols

        return self._requestor.get("ohlc.json", params)
