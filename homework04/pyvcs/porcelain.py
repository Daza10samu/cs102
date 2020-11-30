import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object, resolve_object, read_tree
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def dir_remover(dir: pathlib.Path):
    for dir_path in filter(lambda x: x.is_dir(), dir.glob('*')):
        dir_remover(dir_path)
    if list(dir.glob('*')) == []:
        os.rmdir(str(dir))


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, list(filter(lambda x: x.is_file(), paths)), write=True)
    for path in filter(lambda x: x.is_dir(), paths):
        add(gitdir, list(path.glob("*")))


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    tree = write_tree(gitdir, read_index(gitdir), str(gitdir.parent))
    parent_commit = resolve_head(gitdir)
    com = commit_tree(gitdir, tree, message, parent_commit, author)
    return com


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    for entry in read_index(gitdir):
        try:
            os.remove(entry.name)
        except FileNotFoundError:
            pass
    commit_que = [commit_parse(read_object(obj_name, gitdir)[1])]
    while len(commit_que) != 0:
        comm = commit_que.pop()
        if 'parent' in comm:
            commit_que.append(commit_parse((read_object(comm['parent'], gitdir)[1])))
        tree_que: tp.List[tp.Tuple[pathlib.Path, tp.List[tp.Tuple[int, str, str]]]]
        tree_que = [(gitdir.parent, read_tree(read_object(comm['tree'], gitdir)[1]))]
        while len(tree_que) != 0:
            tree_path, tree_content = tree_que.pop()
            for file_data in tree_content:
                fmt, data = read_object(file_data[2], gitdir)
                if fmt == 'tree':
                    tree_que.append((tree_path / file_data[1], read_tree(data)))
                    try:
                        (tree_path / file_data[1]).mkdir()
                    except FileExistsError:
                        pass
                else:
                    if not (tree_path / file_data[1]).exists():
                        with (tree_path / file_data[1]).open('wb') as f:
                            f.write(data)
                        (tree_path / file_data[1]).chmod(file_data[0])
    for dir in filter(lambda x: x != gitdir and x.is_dir(), gitdir.parent.glob('*')):
        dir_remover(dir)
