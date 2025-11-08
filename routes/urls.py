
from core.router.router import router
from controllers.index import IndexController

routes = [
    {
        "path": "/",
        "method": "GET",
        "controller": IndexController,
        "function": 'index'
    },
    {
        "path": "/about",
        "method": "GET",
        "controller": IndexController,
        "function": 'about'
    }
]

router.register(routes)
