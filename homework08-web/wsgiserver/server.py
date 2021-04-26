import typing
import typing as tp
import socket

from httpserver import BaseHTTPRequestHandler, HTTPServer
from httptools import HttpRequestParser

from .request import WSGIRequest
from .response import WSGIResponse

Address = tp.Tuple[str, int]


class ApplicationType:
    def __call__(self, *args, **kwargs) -> typing.Iterable[bytes]:
        pass


class WSGIServer(HTTPServer):
    def __init__(self, *args, **kwargs) -> None:
        if "request_handler_cls" not in kwargs:
            kwargs["request_handler_cls"] = WSGIRequestHandler
        if "timeout" not in kwargs:
            kwargs["timeout"] = 0.5
        super().__init__(*args, **kwargs)
        self.app: tp.Optional[ApplicationType] = None

    def set_app(self, app: ApplicationType) -> None:
        self.app = app

    def get_app(self) -> tp.Optional[ApplicationType]:
        return self.app


class WSGIRequestHandler(BaseHTTPRequestHandler):
    request_klass = WSGIRequest
    response_klass = WSGIResponse

    def __init__(self, socket: socket.socket, address: Address, server: WSGIServer) -> None:
        self.socket = socket
        self.address = address
        self.server = server

        self.parser = HttpRequestParser(self)

        self._url: bytes = b""
        self._headers: tp.Dict[bytes, bytes] = {}
        self._body_list: tp.List[bytes] = []
        self._parsed = False

    def handle_request(self, request: WSGIRequest) -> WSGIResponse:
        environ = request.to_environ()
        environ["SERVER_NAME"] = self.address[0]
        environ["SERVER_PORT"] = self.address[1]
        response = WSGIResponse()
        app = self.server.get_app()
        body_iterable = app(environ, response.start_response)
        response.body = b"".join(body_iterable)
        return response
