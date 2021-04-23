import datetime
import mimetypes
import pathlib
import time
import typing as tp
from socketserver import BaseRequestHandler
from urllib.parse import unquote, urlparse

from httpserver import BaseHTTPRequestHandler, HTTPRequest, HTTPResponse, HTTPServer


def path_resolver(path: str) -> str:
    splitted = path.split("/")
    curr: tp.List[str] = []
    for i in splitted:
        if i == "..":
            try:
                curr.pop()
            except IndexError:
                pass
        elif i == ".":
            continue
        else:
            curr.append(i)
    try:
        if "." in curr[-2] and curr[-1] == "":
            del curr[-1]
    except IndexError:
        pass
    curr[-1] = curr[-1].split("?", 1)[0]
    return "/".join(curr)


def url_normalize(path: str) -> str:
    normalized_path = path_resolver(path.replace("//", "/"))[1:]
    return unquote(normalized_path) + (
        "index.html" if len(normalized_path) == 0 or normalized_path[-1] == "/" else ""
    )


class StaticHTTPRequestHandler(BaseHTTPRequestHandler):  # type:ignore
    def __init__(self, *args, **kwargs) -> None:  # type:ignore
        super().__init__(*args, **kwargs)
        self.document_root = pathlib.Path(document_root)
        self._url: bytes = b""
        self._headers: tp.Dict[bytes, bytes] = {}
        self._body: bytes = b""
        self._parsed = False

    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        # NOTE: https://tools.ietf.org/html/rfc3986
        # NOTE: echo -n "GET / HTTP/1.0\r\n\r\n" | nc localhost 5000
        headers = {
            "Server": "too simple to live service",
            "Date": datetime.datetime.now().strftime("%a, %d %b %Y %H:%m:%S"),
            "Allow": "GET, HEAD",
        }

        if request.method == b"PUSH" and request.body == b"":
            return HTTPResponse(400, headers, b"")
        if request.method not in (b"GET", b"HEAD"):
            return HTTPResponse(405, headers, b"")

        if request.method == b"HEAD":
            headers["Content-Type"] = mimetypes.types_map.get(
                "." + url_normalize(request.url.decode()).rsplit(".", 1)[1], ""
            )
            return HTTPResponse(200, headers, b"")

        try:
            file_path = self.document_root / url_normalize(request.url.decode())
            with file_path.open("rb") as f:
                data = f.read()
                headers["Content-Length"] = str(len(data))
                headers["Content-Type"] = mimetypes.types_map.get(
                    "." + url_normalize(request.url.decode()).rsplit(".", 1)[1], ""
                )

                return HTTPResponse(200, headers, data)

        except FileNotFoundError:
            return HTTPResponse(404, headers, b"")


class StaticServer(HTTPServer):  # type:ignore
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8080,
        document_root: pathlib.Path = pathlib.Path("/tmp"),
        backlog_size: int = 1,
        max_workers: int = 1,
        timeout: tp.Optional[float] = None,
        request_handler_cls: tp.Type[BaseRequestHandler] = StaticHTTPRequestHandler,  # type:ignore
    ):
        super().__init__(
            host, port, backlog_size, max_workers, timeout, request_handler_cls  # type:ignore
        )
        self.document_root = document_root


if __name__ == "__main__":
    document_root = pathlib.Path("static") / "root"
    server = StaticServer(
        port=5000,
        max_workers=5,
        timeout=2,
        document_root=document_root,
        request_handler_cls=StaticHTTPRequestHandler,  # type:ignore
    )
    server.serve_forever()
