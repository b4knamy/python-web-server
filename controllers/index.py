from core.controllers.controller import Controller
from core.http.response import JSONResponse


class IndexController(Controller):

    def index(self, request):
        return JSONResponse(data={
            "ok": True
        })

    def about(self, request):
        return {
            "about": "well, wants to know more about me, huh?"
        }
