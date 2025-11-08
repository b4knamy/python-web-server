from abc import ABC

from core.http.response import JSONResponse


class BaseError(ABC, Exception):
    message: str
    status: int
    trace_back: Exception
    action: str
    is_internal: bool

    def __init__(self, message=None, status=None, action=None, trace_back=None, is_internal=False):
        self.message = message or self.message
        self.status = status or self.status
        self.action = action or self.action
        self.trace_back = trace_back or self.trace_back
        self.is_internal = is_internal

    def to_json(self):
        if self.is_internal:
            print(f"\n\nERROR - {self.message}, {self.action}\n\n")

            return JSONResponse(data={
                "name": "InternalServerError",
                "message": "Something went wrong in our server.",
                "status": 500,
                "action": "Please, try again later."
            }, status=500)

        return JSONResponse(data=self.get_data(), status=self.status)

    def get_data(self):
        return {
            "name": self.__class__.__name__,
            "message": self.message,
            "status": self.status,
            "action": self.action
        }


class InternalServerError(BaseError):

    message = "Something went wrong in our server."
    status = 500
    trace_back: Exception = None
    action = "Please, try again later."


class NotFoundError(BaseError):
    message = "Content not found"
    status = 404
    trace_back: Exception = None
    action = "Check parameters to see if it is correct"


class MethodNotAllowedError(BaseError):
    status = 405
    trace_back: Exception = None
