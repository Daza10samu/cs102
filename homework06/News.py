import typing as tp
from dataclasses import dataclass


@dataclass
class News:
    id: int
    title: str
    author: str
    url: str
    comments: int
    points: int
    label: tp.Optional[str]
