from __future__ import annotations

import socket
import typing as tp

from httptools import HttpRequestParser
from httptools.parser.errors import *

from .request import HTTPRequest
from .response import HTTPResponse

if tp.TYPE_CHECKING:
    from .server import TCPServer

Address = tp.Tuple[str, int]


class BaseRequestHandler:
    def __init__(self, socket: socket.socket, address: Address, server: TCPServer) -> None:
        self.socket = socket
        self.address = address
        self.server = server

    def handle(self) -> None:
        self.close()

    def close(self) -> None:
        self.socket.close()


class EchoRequestHandler(BaseRequestHandler):
    def handle(self) -> None:
        try:
            data = self.socket.recv(1024)
        except (socket.timeout, BlockingIOError):
            pass
        else:
            self.socket.sendall(data)
        finally:
            self.close()


class BaseHTTPRequestHandler(BaseRequestHandler):
    request_klass = HTTPRequest
    response_klass = HTTPResponse

    def __init__(self, *args, **kwargs) -> None:  # type:ignore
        super().__init__(*args, **kwargs)
        self.parser = HttpRequestParser(self)

        self._url: bytes = b""
        self._headers: tp.Dict[bytes, bytes] = {}
        self._body: bytes = b""
        self._parsed = False

    def handle(self) -> None:
        request = self.parse_request()
        if request:
            try:
                response = self.handle_request(request)
            except Exception:
                # TODO: log exception
                response = self.response_klass(status=500, headers={}, body=b"")
        else:
            response = self.response_klass(status=400, headers={}, body=b"")
        self.handle_response(response)
        self.close()

    def parse_request(self) -> tp.Optional[HTTPRequest]:
        while not self._parsed:
            try:
                data = self.socket.recv(65536)
            except (
                socket.timeout,
                BlockingIOError,
            ):
                break
            if data == b"":
                break
            try:
                self.parser.feed_data(data)
            except (
                HttpParserError,  # type: ignore
                HttpParserInvalidMethodError,  # type: ignore
                HttpParserInvalidURLError,  # type: ignore
                HttpParserCallbackError,  # type: ignore
                HttpParserInvalidStatusError,  # type: ignore
                HttpParserUpgrade,  # type: ignore
            ):
                break
        if self._parsed:
            return self.request_klass(
                self.parser.get_method(), self._url, self._headers, self._body
            )
        return None

    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        return self.response_klass(200, {}, b"ok")

    def handle_response(self, response: HTTPResponse) -> None:
        self.socket.sendall(response.to_http1())

    def on_url(self, url: bytes) -> None:
        self._url = url

    def on_header(self, name: bytes, value: bytes) -> None:
        self._headers[name] = value

    def on_body(self, body: bytes) -> None:
        self._body = body

    def on_message_complete(self) -> None:
        self._parsed = True
