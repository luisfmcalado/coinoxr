from coinoxr.requestor import Requestor


class Usage:
    def __init__(self, requestor=None):
        self._requestor = requestor
        if requestor is None:
            self._requestor = Requestor()

    def get(self, pretty_print=False):
        params = {"prettyprint": pretty_print}
        return self._requestor.get("usage.json", params)
