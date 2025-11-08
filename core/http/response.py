from abc import ABC, abstractmethod
import json


class Response(ABC):

    def __init__(self, data, status=200, headers=None):
        self.data = data
        self.status = status
        self.headers = headers or {}

    def send(self):
        body = self.get_body()

        response = (
            f"{self.get_status_line()}\r\n"
            f"{self.get_headers_line(body)}\r\n"
            f"{body}"
        )

        return response.encode('utf-8')

    def get_status_line(self):
        status_messages = {
            200: "OK",
            201: "Created",
            204: "No Content",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            500: "Internal Server Error",
        }

        return f"HTTP/1.1 {self.status} {status_messages.get(self.status, 'Unknown')}"

    def get_headers_line(self, body):

        if not self.content_type:
            raise AttributeError(
                "Subclasses must set 'content_type' attribute")

        headers = {
            "Content-Type": f"{self.content_type}; charset=utf-8",
            "Content-Length": str(len(body.encode('utf-8'))),
            **self.headers,  # permite sobrescrever headers padrões
        }

        # Junta todos os headers em uma string
        header_lines = "".join(f"{k}: {v}\r\n" for k, v in headers.items())
        return header_lines

    @abstractmethod
    def get_body(self):
        pass


class JSONResponse(Response):
    content_type = 'application/json'

    def get_body(self):
        return json.dumps(self.data)


class HTMLResponse(Response):
    content_type = 'text/html'

    def get_body(self):
        return str(self.data)
