from coinoxr.requestor import Requestor


class TimeSeries:
    def __init__(self, requestor=None):
        self._requestor = requestor
        if requestor is None:
            self._requestor = Requestor()

    def get(
        self,
        start,
        end,
        base=None,
        pretty_print=False,
        symbols=None,
        show_alternative=False,
    ):
        params = {
            "prettyprint": pretty_print,
            "show_alternative": show_alternative,
            "start": start,
            "end": end,
        }

        if base is not None:
            params["base"] = base

        if symbols is not None:
            params["symbols"] = symbols

        return self._requestor.get("time-series.json", params)
