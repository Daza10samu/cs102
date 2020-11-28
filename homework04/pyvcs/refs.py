import pathlib
import typing as tp
import os


def update_ref(
        gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str
) -> None:
    with (gitdir / ref).open('w') as f:
        f.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    with (gitdir / 'HEAD').open('w') as f:
        f.write(name)


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    if refname == 'HEAD' and not is_detached(gitdir):
        return resolve_head(gitdir)
    if (gitdir / refname).exists():
        with (gitdir / refname).open() as f:
            return f.read().strip()
    return None


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    return ref_resolve(gitdir, get_ref(gitdir))


def is_detached(gitdir: pathlib.Path) -> bool:
    with (gitdir / 'HEAD').open() as f:
        data = f.read().strip()
    return len(data) == 40


def get_ref(gitdir: pathlib.Path) -> str:
    with (gitdir / 'HEAD').open() as f:
        return f.read().split(' ')[1].strip()
