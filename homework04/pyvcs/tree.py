import hashlib
import os
import pathlib
import datetime
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index, update_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(
        gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = ""
) -> str:
    path = gitdir.parent / dirname
    files = list(path.glob('*'))
    unhandled_dirs = dict()
    enties_to_format = []
    for entry in index:
        entry_file = pathlib.Path(entry.name)
        if entry_file in files:
            enties_to_format.append(entry)
        else:
            dir_name = entry.name.lstrip(dirname).split('/', 1)[0]
            if not dir_name in unhandled_dirs:
                unhandled_dirs[dir_name] = []
            unhandled_dirs[dir_name].append(entry)
    for dir_name in unhandled_dirs:
        stat = (pathlib.Path(dirname) / dir_name).stat()
        sha = write_tree(gitdir, unhandled_dirs[dir_name], dir_name)
        enties_to_format.append(GitIndexEntry(ctime_s=int(stat.st_ctime),
                                              ctime_n=int(str(stat.st_ctime_ns)[len(str(int(stat.st_ctime))):]),
                                              mtime_s=int(stat.st_mtime),
                                              mtime_n=int(str(stat.st_mtime_ns)[len(str(int(stat.st_mtime))):]),
                                              dev=stat.st_dev,
                                              ino=stat.st_ino,
                                              mode=0o40000,  # mode for git tree
                                              uid=stat.st_uid,
                                              gid=stat.st_gid,
                                              size=stat.st_size,
                                              sha1=bytes.fromhex(sha),
                                              flags=7,
                                              name=str(pathlib.Path(dirname) / dir_name)))
    preformatted_data = b''.join(
        oct(entry.mode)[2:].encode() + b' ' + pathlib.Path(entry.name).name.encode() + b'\x00' + entry.sha1 for entry in
        sorted(enties_to_format, key=lambda x: x.name))
    return hash_object(preformatted_data, 'tree', write=True)


def commit_tree(
        gitdir: pathlib.Path,
        tree: str,
        message: str,
        parent: tp.Optional[str] = None,
        author: tp.Optional[str] = None,
) -> str:
    now_bad_format = time.localtime()
    now = int(datetime.datetime(year=now_bad_format.tm_year, day=now_bad_format.tm_mday, month=now_bad_format.tm_mon,
                                hour=now_bad_format.tm_hour, minute=now_bad_format.tm_min,
                                second=now_bad_format.tm_sec).timestamp())
    tz = time.timezone
    tz_str = ('-' if tz > 0 else '+') + f'{abs(tz) // 3600:02}{abs(tz) // 60 % 60:02}'
    data = (f'tree {tree}\nauthor {author} {now} {tz_str}\ncommitter {author} {now} {tz_str}' +
            f'\n{"" if parent is None else parent}\n{message}\n').encode()
    return hash_object(data, 'commit', write=True)
