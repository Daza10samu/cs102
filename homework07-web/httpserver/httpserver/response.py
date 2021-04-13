import dataclasses
import http
import typing as tp


@dataclasses.dataclass
class HTTPResponse:
    status: int
    headers: tp.Dict[str, str] = dataclasses.field(default_factory=dict)
    body: bytes = b""

    def to_http1(self) -> bytes:
        return (f"HTTP/1.0 {self.status}\r\n" + ', \r\n'.join(
            f"{x}: {self.headers[x]}" for x in self.headers) + "\r\n\r\n").encode() + self.body
