from os import path
import json
import datetime

from coinoxr.response import Response
from coinoxr.client import HttpClient
from urllib.parse import urlparse


class StubHttpClient(HttpClient):
    def __init__(self):
        self._app_ids = []
        self._dates = []

    def get(self, url, params):
        route = urlparse(url).path.split("/")
        filename = route[-1].replace(".json", "")

        amount = None
        from_currency = None
        to_currency = None
        if "convert" in route:
            filename = "convert"
            amount = route[-3]
            from_currency = route[-2]
            to_currency = route[-1]
        file_path = "tests/fixtures/%s.json" % filename

        if not path.isfile(file_path) and "historical" not in route:
            return Response(404, None)

        if "ohlc.json" in route and not self.valid_start_time(params["start_time"]):
            response = self.json("tests/fixtures/invalid_start_time.json")
            return Response(response["code"], response["content"])

        if "ohlc.json" in route and not self.valid_start_point(params["period"]):
            response = self.json("tests/fixtures/invalid_period_start_point.json")
            return Response(response["code"], response["content"])

        if "historical" in route and not self.valid_date(filename):
            response = self.json("tests/fixtures/invalid_date.json")
            return Response(response["code"], response["content"])

        if "historical" in route and self.missing_date(filename):
            response = self.json("tests/fixtures/date_not_available.json")
            return Response(response["code"], response["content"])

        if filename in ["time-series"] and not self.valid_range(params):
            response = self.json("tests/fixtures/invalid_date_range.json")
            return Response(response["code"], response["content"])

        if filename in ["time-series"] and not self.range_available(params):
            response = self.json("tests/fixtures/range_not_available.json")
            return Response(response["code"], response["content"])

        if filename not in ["currencies"] and not self.valid_app_id(params):
            response = self.json("tests/fixtures/invalid_app_id.json")
            return Response(response["code"], response["content"])

        if filename not in ["currencies"] and self.missing_app_id(params):
            response = self.json("tests/fixtures/missing_app_id.json")
            return Response(response["code"], response["content"])

        if not self.valid_conversion(from_currency, to_currency):
            response = self.json("tests/fixtures/invalid_currency.json")
            return Response(response["code"], response["content"])

        if amount is not None and int(amount) < 0:
            response = self.json("tests/fixtures/invalid_amount.json")
            return Response(response["code"], response["content"])

        response = self.json(file_path)
        return Response(response["code"], response["content"])

    def add_app_id(self, app_id):
        self._app_ids.append(app_id)

    def add_date(self, date):
        self._dates.append(date)

    def missing_app_id(self, params):
        return params["app_id"] not in self._app_ids

    def missing_date(self, date):
        return date not in self._dates

    def range_available(self, params):
        return not self.missing_date(params["start"]) and not self.missing_date(
            params["end"]
        )

    @classmethod
    def valid_range(cls, params):
        return cls.valid_date(params["start"]) and cls.valid_date(params["end"])

    @classmethod
    def valid_conversion(cls, from_currency, to_currency):
        return cls.valid_currency(from_currency) and cls.valid_currency(to_currency)

    @classmethod
    def valid_currency(cls, currency):
        return currency is None or len(currency) == 3

    @classmethod
    def valid_start_time(cls, start_time):
        return cls.valid_datetime(start_time)

    @classmethod
    def valid_start_point(cls, period):
        return period in ["30m"]

    @classmethod
    def valid_app_id(cls, params):
        return len(params["app_id"]) > 3

    @classmethod
    def valid_date(cls, date):
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            pass
        return False

    @classmethod
    def valid_datetime(cls, date):
        try:
            datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
            return True
        except ValueError:
            pass
        return False

    @staticmethod
    def json(file):
        content = None
        with open(file) as f:
            content = json.load(f)
        return content
