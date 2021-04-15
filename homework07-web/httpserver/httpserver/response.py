import dataclasses
import http
import typing as tp

code_to_status = {200: "OK", 400: "Bad Request", 404: "Not Found"}


@dataclasses.dataclass
class HTTPResponse:
    status: int
    headers: tp.Dict[str, str] = dataclasses.field(default_factory=dict)
    body: bytes = b""

    def to_http1(self) -> bytes:
        return (
            f"HTTP/1.1 {self.status} {code_to_status.get(self.status, '')}\r\n"
            + "\r\n".join(f"{x}: {self.headers[x]}" for x in self.headers)
            + "\r\n\r\n"
        ).encode() + self.body
