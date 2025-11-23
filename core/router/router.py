from core.router.middlewares import global_middlewares


class Router:
    routes = []
    middlewares = [middlewares for middlewares in global_middlewares]

    def register(self, incoming_routes):
        for route in incoming_routes:
            self.routes.append(route)

    def add_middleware(self, func):
        self.middlewares.append(func)

    def get(self, path: str):
        for route in self.routes:
            if route["path"] == path:
                return route


router = Router()
