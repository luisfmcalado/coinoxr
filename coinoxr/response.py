from dataclasses import dataclass


@dataclass
class Response:
    code: int
    body: dict or None
