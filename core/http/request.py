

from core.exceptions.exceptions import MethodNotAllowedError, NotFoundError
from core.http.response import JSONResponse
from core.parsers.request_parser import parse_http_request


class Request:
    method: str
    path: str
    headers: dict[str: any]
    body: any

    def __init__(self, data):
        request = parse_http_request(data)

        self.method = request["method"]
        self.path = request["path"]
        self.headers = request["headers"]
        self.body = request["body"]

        print("👉 Método:", request["method"])
        print("👉 Caminho:", request["path"])
        print("👉 Headers:", request["headers"])
        print("👉 Corpo:", request["body"])

    def __str__(self):
        return f'====================================\nPATH: {self.path}\nMETHOD: {self.method}\n===================================='


class RequestResolver:

    def __init__(self, data, router):
        self.data = data
        self.router = router
        self.request = None

    def resolve(self):

        self.request = Request(self.data)

        route = self.router.get(self.request.path)

        if not route:
            raise NotFoundError(
                message="Route not found",
                action="Try another route"
            )

        if not route.get("method") == self.request.method:
            raise MethodNotAllowedError(
                message=f"Method '{self.request.method}' not allowed.",
                action="Try another method"
            )

        controller_cls = route.get("controller")

        if not controller_cls:
            return NotFoundError(
                message="Controller not found",
                action="Check the router registry"
            )

        controller = controller_cls()

        response = controller.handler(route.get('function'), self.request)

        return response
