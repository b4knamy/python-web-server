
from __future__ import annotations
from typing import TYPE_CHECKING
from core.exceptions.exceptions import BaseError
from core.settings import THROTTLE_REQUESTS_LIMIT, THROTTLE_REQUESTS_TIMEOUT
import time

if TYPE_CHECKING:
    from core.http.request import Request

request_times = {}


class ThrottleError(BaseError):
    message = "Too many requests attempts"
    status = 429
    trace_back = None
    action = "Wait a fews minutes to make another request"


def throttle_middleware(request: Request):
    now = time.time()

    timestamps = request_times.get(request.ip, [])

    updated_timestamps = [
        t for t in timestamps if now - t < THROTTLE_REQUESTS_TIMEOUT
    ]
    timestamps_length = len(updated_timestamps)

    if timestamps_length > THROTTLE_REQUESTS_LIMIT:
        raise ThrottleError()

    updated_timestamps.append(now)
    request_times[request.ip] = updated_timestamps

    request.context["headers"]["X-RateLimit-Limit"] = str(
        THROTTLE_REQUESTS_LIMIT)
    request.context["headers"]["X-RateLimit-Remaining"] = str(
        THROTTLE_REQUESTS_LIMIT - timestamps_length)
