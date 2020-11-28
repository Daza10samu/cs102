import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    git_dir = ".pyvcs"
    if os.environ["GIT_DIR"]:
        git_dir = os.environ["GIT_DIR"]
    path = pathlib.Path(workdir)
    while path.absolute() != pathlib.Path('/'):
        if (path / git_dir).exists():
            return path / git_dir
        path = path.parent
    if (path / git_dir).exists():
        return path / git_dir
    raise ValueError('Not a git repository')


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    if pathlib.Path(workdir).is_file():
        raise ValueError(f"{workdir} is not a directory")
    git_dir = ".pyvcs"
    if "GIT_DIR" in os.environ:
        git_dir = os.environ["GIT_DIR"]
    path = pathlib.Path(workdir) / git_dir
    path.mkdir()
    (path / 'refs').mkdir()
    (path / 'refs' / 'heads').mkdir()
    (path / 'refs' / 'tags').mkdir()
    (path / 'objects').mkdir()
    with (path / 'HEAD').open('w') as f:
        f.write('ref: refs/heads/master\n')
    with (path / 'config').open('w') as f:
        f.write(
            '[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n')
    with (path / 'description').open('w') as f:
        f.write('Unnamed pyvcs repository.\n')
    return path
