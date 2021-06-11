import dataclasses
import io
import json
import typing as tp


@dataclasses.dataclass
class Request:
    path: str
    method: str
    query: tp.Dict[str, str] = dataclasses.field(default_factory=dict)
    body: io.BytesIO = dataclasses.field(default_factory=io.BytesIO)
    headers: tp.Dict[str, str] = dataclasses.field(default_factory=dict)

    def text(self) -> tp.Optional[str]:
        return self.body.read().decode()

    def json(self) -> tp.Optional[tp.Dict[str, tp.Any]]:
        return json.loads(self.text())  # type:ignore
