from coinoxr.requestor import Requestor


class Currency:
    def __init__(self, requestor=None):
        self._requestor = requestor
        if requestor is None:
            self._requestor = Requestor(skip_app_id=True)

    def get(
        self, pretty_print=False, show_alternative=False, show_inactive=False,
    ):
        params = {
            "prettyprint": pretty_print,
            "show_alternative": show_alternative,
            "show_inactive": show_inactive,
        }
        return self._requestor.get("currencies.json", params)
