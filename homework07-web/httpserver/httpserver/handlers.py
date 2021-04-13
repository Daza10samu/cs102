from __future__ import annotations

import socket
import typing as tp

from . import parsers

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

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
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
        total_data = b''
        try:
            while 1:
                data = self.socket.recv(65536)
                if data:
                    total_data += data
                else:
                    break
        except (socket.timeout, BlockingIOError):
            pass
        return parsers.request_parser(total_data)

    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        return HTTPResponse(200, {}, b"ok")

    def handle_response(self, response: HTTPResponse) -> None:
        self.socket.sendall(response.to_http1())

    def on_url(self, url: bytes) -> None:
        pass

    def on_header(self, name: bytes, value: bytes) -> None:
        pass

    def on_body(self, body: bytes) -> None:
        pass

    def on_message_complete(self) -> None:
        pass
