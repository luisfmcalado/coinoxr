import requests
from coinoxr.response import Response


class HttpClient:
    def get(self, url, params):
        return Response(200, None)


class RequestsClient(HttpClient):
    def get(self, url, params):
        response = requests.get(url, params=params)
        try:
            return Response(response.status_code, response.json())
        except ValueError:
            return Response(response.status_code, None)
