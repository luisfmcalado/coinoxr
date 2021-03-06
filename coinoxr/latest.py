from coinoxr.requestor import Requestor


class Latest:
    def __init__(self, requestor=None):
        self._requestor = requestor
        if requestor is None:
            self._requestor = Requestor()

    def get(self, base=None, pretty_print=False, symbols=None, show_alternative=False):
        params = {"prettyprint": pretty_print, "show_alternative": show_alternative}

        if base is not None:
            params["base"] = base

        if symbols is not None:
            params["symbols"] = symbols

        return self._requestor.get("latest.json", params)
