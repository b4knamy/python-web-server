from core.exceptions.exceptions import NotFoundError
from core.http.response import JSONResponse


class Controller:

    def handler(self, function_name: str, request):

        function_handler = getattr(self, function_name, None)

        if not function_handler:
            raise NotFoundError(
                message="Controller handler not found",
                action="Check the router registry",
                is_internal=True
            )

        response = function_handler(request)
        return response if isinstance(response, JSONResponse) else JSONResponse(response)
