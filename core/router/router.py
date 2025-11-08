class Router:
    urls_path = []

    def register(self, routes):
        for route in routes:
            self.urls_path.append(route)

    def get(self, path: str):
        for url in self.urls_path:
            if url["path"] == path:
                return url


router = Router()
