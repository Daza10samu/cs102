import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        return (
                self.ctime_s.to_bytes(4, "big")
                + self.ctime_n.to_bytes(4, "big")
                + self.mtime_s.to_bytes(4, "big")
                + self.mtime_n.to_bytes(4, "big")
                + self.dev.to_bytes(4, "big")
                + self.ino.to_bytes(4, "big")
                + self.mode.to_bytes(4, "big")
                + self.uid.to_bytes(4, "big")
                + self.gid.to_bytes(4, "big")
                + self.size.to_bytes(4, "big")
                + self.sha1
                + self.flags.to_bytes(2, "big")
                + self.name.encode()
                + b"\x00" * (8 - (62 + len(self.name.encode())) % 8)
        )

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        return GitIndexEntry(
            ctime_s=int.from_bytes(data[:4], byteorder="big"),
            ctime_n=int.from_bytes(data[4:8], byteorder="big"),
            mtime_s=int.from_bytes(data[8:12], byteorder="big"),
            mtime_n=int.from_bytes(data[12:16], byteorder="big"),
            dev=int.from_bytes(data[16:20], byteorder="big"),
            ino=int.from_bytes(data[20:24], byteorder="big"),
            mode=int.from_bytes(data[24:28], byteorder="big"),
            uid=int.from_bytes(data[28:32], byteorder="big"),
            gid=int.from_bytes(data[32:36], byteorder="big"),
            size=int.from_bytes(data[36:40], byteorder="big"),
            sha1=data[40:60],
            flags=int.from_bytes(data[60:62], byteorder="big"),
            name=data[62:].strip(b"\x00").decode(),
        )


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    if not (gitdir / "index").is_file():
        return []
    with (gitdir / "index").open("rb") as f:
        data = f.read()
    headers, data = data[:12], data[12:]
    count = int.from_bytes(headers[8:], "big")
    entries = []
    for _ in range(count):
        pos = len(data)
        for i in range(64, len(data) + 1, 8):
            if data[i - 1] == 0:
                pos = i
                break
        entries.append(GitIndexEntry.unpack(data[:pos]))
        data = data[pos:]
    return entries


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    data = b""
    data += b"DIRC\x00\x00\x00\x02"
    data += len(entries).to_bytes(4, "big")
    for entry in entries:
        data += entry.pack()
    data += hashlib.sha1(data).digest()
    with (gitdir / "index").open("wb") as f:
        f.write(data)


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    entries = read_index(gitdir)
    if not details:
        print(*[x.name for x in entries], sep="\n")
    else:
        print(
            *[f"{oct(x.mode)[2:]} {x.sha1.hex()} 0\t{x.name}" for x in entries],
            sep="\n",
        )


def update_index(
        gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True
) -> None:
    entries = read_index(gitdir)
    names = map(lambda x: x.name, entries)
    for path in paths:
        with path.open("rb") as f:
            data = f.read()
        stat = path.stat()
        if str(path) in names:
            del_ind = names.index(str(path))
            del entries[del_ind]
            del names[del_ind]
        sha1_hash = hash_object(data, "blob")
        try:
            (gitdir / 'objects').mkdir()
        except FileExistsError:
            pass
        try:
            (gitdir / 'objects' / sha1_hash[:2]).mkdir()
        except FileExistsError:
            pass
        with (gitdir / 'objects' / sha1_hash[:2] / sha1_hash[2:]).open('wb') as f:
            f.write(data)
        entries.append(
            GitIndexEntry(
                ctime_s=int(stat.st_ctime),
                ctime_n=int(str(stat.st_ctime_ns)[len(str(int(stat.st_ctime))):]),
                mtime_s=int(stat.st_mtime),
                mtime_n=int(str(stat.st_mtime_ns)[len(str(int(stat.st_mtime))):]),
                dev=stat.st_dev,
                ino=stat.st_ino,
                mode=stat.st_mode,
                uid=stat.st_uid,
                gid=stat.st_gid,
                size=stat.st_size,
                sha1=bytes.fromhex(sha1_hash),
                flags=7,
                name=str(path),
            )
        )
    if write:
        entries.sort(key=lambda x: x.name)
        write_index(gitdir, entries)
