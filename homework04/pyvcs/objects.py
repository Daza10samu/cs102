import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    formatted_data = (fmt + f" {len(data)}\0").encode() + data
    hash_str = hashlib.sha1(formatted_data).hexdigest()
    if write:
        dir_path = repo_find('.') / 'objects'
        try:
            dir_path /= hash_str[:2]
            dir_path.mkdir()
        except FileExistsError:
            pass
        with (dir_path / hash_str[2:]).open('wb') as f:
            f.write(zlib.compress(formatted_data))
    return hash_str


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if len(obj_name) < 4:
        raise ValueError(f"Not a valid object name {obj_name}")
    object_dir = gitdir / 'objects'
    result = list(map(lambda x: ''.join(str(x).split('/')[-2:]), (object_dir / obj_name[:2]).glob(f'{obj_name[2:]}*')))
    if len(result) == 0:
        raise ValueError(f"Not a valid object name {obj_name}")
    return result


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    object_dir = gitdir / 'objects'
    with (object_dir / sha[:2] / sha[2:]).open('rb') as f:
        file_content = zlib.decompress(f.read())
    extra_data, main_content = file_content.split(b'\x00', maxsplit=1)
    b_fmt: bytes
    b_length: bytes
    b_fmt, b_length = extra_data.split()
    fmt = b_fmt.decode()
    length = int(b_length)
    if length != len(main_content):
        raise ValueError(f'Object {sha} is damaged')
    return fmt, main_content


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    data_list = (b'\x00' + b'\x01' * 20 + data).split(b'\x00')
    result = []
    for i in range(1, len(data_list) - 1):
        *main_data, = data_list[i][20:].decode().split(' ')
        sha = data_list[i + 1][:20]
        result.append((int(main_data[0]), main_data[1], sha.hex()))
    return result


def cat_file(obj_name: str, pretty: bool = True) -> None:
    data = read_object(obj_name, repo_find('.'))
    if data[0] in ('blob', 'commit'):
        out = data[1].decode()
        if pretty:
            print(out)
        else:
            print(data[0], out)
    elif data[0] == 'tree':
        out = read_tree(data[1])
        if pretty:
            print(*[f'{x[0]:06} {"tree" if x[0] == 40000 else "blob"} {x[2]}\t{x[1]}' for x in out], sep='\n')


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
