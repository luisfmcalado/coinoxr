import coinoxr
from coinoxr.error import AppIdError


class Requestor:
    def __init__(self, app_id=None, client=None, skip_app_id=False):
        self._client = coinoxr.default_http_client
        self._skip_app_id = skip_app_id
        if client is not None:
            self._client = client

        self._app_id = coinoxr.app_id
        if app_id is not None:
            self._app_id = app_id

        if not skip_app_id and not isinstance(self._app_id, str):
            raise AppIdError(
                "No API key provided. Setup coinoxr.app_id = <API-Key> or app_id argument."
                "You can get the API key from open exchange rates dashboard."
            )

    def get(self, path, params):
        url = coinoxr.base_url(path)

        if not self._skip_app_id:
            params = {**params, "app_id": self._app_id}

        return self._client.get(url, params=params)
