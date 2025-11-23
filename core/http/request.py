
from __future__ import annotations
from core.exceptions.exceptions import MethodNotAllowedError, NotFoundError
from core.http.response import JSONResponse, Response
from core.parsers.request_parser import parse_http_request
from core.router.router import Router


class Request:
    method: str
    path: str
    headers: dict[str: any]
    body: any
    ip: str
    context: dict

    def __init__(self, data, ip):
        request = parse_http_request(data)

        self.method = request["method"]
        self.path = request["path"]
        self.headers = request["headers"]
        self.body = request["body"]
        self.ip = ip
        self.context = {
            "headers": {}
        }

        # print("👉 Método:", request["method"])
        # print("👉 Caminho:", request["path"])
        # print("👉 Headers:", request["headers"])
        # print("👉 Corpo:", request["body"])

    def __str__(self):
        return f'====================================\nPATH: {self.path}\nMETHOD: {self.method}\n===================================='


class RequestResolver:

    def __init__(self, data, router: Router, ip):
        self.router = router
        self.request = Request(data, ip)
        self.middlewares = []

    def resolve(self):
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
                action="Check the router registry",
                is_internal=True
            )

        self.handle_middlewares(extra_middlewares=route.get('middlewares', []))

        controller = controller_cls()

        response = controller.handler(route.get('function'), self.request)
        response.insert_headers(self.request.context["headers"])

        return response

    def handle_middlewares(self, extra_middlewares: list):
        for middleware in self.router.middlewares:
            middleware(self.request)

        for extra_middleware in extra_middlewares:
            extra_middleware(self.request)
