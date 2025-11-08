
def allowed_methods(methods: list):

    def decorator(func):
        def wrapper(*args, **kwargs):
            if not args[0]["method"] in methods:
                return "<h1>405 Method Not Allowed</h1>", "HTTP/1.1 405 METHOD NOT ALLOWED"

            print(f'methods alloweds -> {methods}')
            print(f'Args -> {args}')
            print(f'Kwargs -> {kwargs}')
            return func(*args, **kwargs)

        return wrapper

    return decorator
