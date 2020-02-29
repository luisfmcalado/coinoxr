from coinoxr.requestor import Requestor


class Convert:
    def __init__(self, requestor=None):
        self._requestor = requestor
        if requestor is None:
            self._requestor = Requestor()

    def get(self, amount, from_currency, to_currency, pretty_print=False):
        path = "convert/%s/%s/%s" % (amount, from_currency, to_currency)
        params = {"prettyprint": pretty_print}
        return self._requestor.get(path, params)
