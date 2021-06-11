import http.client
import json
import typing as tp
from urllib.parse import parse_qsl

from slowapi.request import Request
from slowapi.response import JsonResponse, Response
from slowapi.router import Route


class SlowAPI:
    def __init__(self):
        self.routes: tp.List[Route] = []
        self.middlewares = []

    def __call__(self, environ, start_response):
        route = self._find_route(environ)

        args = self._get_args(route, environ)

        query_string = environ["QUERY_STRING"]
        query: tp.Dict[str, str] = dict()
        for i in parse_qsl(query_string):
            query[str(i[0])] = str(i[1])

        request = Request(
            environ["PATH_INFO"], environ["REQUEST_METHOD"], query, environ["wsgi.input"], environ
        )
        response = route.func(request, *args)
        start_response(
            f"{response.status} {http.client.responses[response.status]}", response.headers
        )

        return [str(response).encode()]

    def _find_route(self, environ) -> Route:
        curr_routes = []
        for route in self.routes:
            if route.method == environ["REQUEST_METHOD"] and environ["PATH_INFO"] == route.path:
                curr_routes.append(route)
        if len(curr_routes) == 0:
            for route in self.routes:
                if (
                    route.method == environ["REQUEST_METHOD"]
                    and environ["PATH_INFO"].rsplit("/", 1)[0] == route.path.rsplit("/", 1)[0]
                ):
                    curr_routes.append(route)

            if len(curr_routes) == 0:
                raise Exception("Routes error")

        return curr_routes[0]

    def _get_args(self, route: Route, environ) -> tp.List[str]:
        if "{" in route.path:
            args = environ["PATH_INFO"][route.path.find("{") :].split("&")
            if len(args) == 1 and args[0] == "":
                args = []
        else:
            args = []
        return args

    def route(self, path=None, method=None, **options):
        def inner(func):
            self.routes.append(Route(path, method, func))
            return self.route(path, method="GET", func=func)

        return inner

    def get(self, path=None, **options):
        return self.route(path, method="GET", **options)

    def post(self, path=None, **options):
        return self.route(path, method="POST", **options)

    def patch(self, path=None, **options):
        return self.route(path, method="PATCH", **options)

    def put(self, path=None, **options):
        return self.route(path, method="PUT", **options)

    def delete(self, path=None, **options):
        return self.route(path, method="DELETE", **options)

    def add_middleware(self, middleware) -> None:
        self.middlewares.append(middleware)
