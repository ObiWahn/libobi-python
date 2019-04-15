from pathlib import Path

def remove_from_front(path:Path, *args):
    parts = list(path.parts)
    for arg in args:
        if parts[0] == arg:
            parts = parts[1:]
        else:
            return path
    return Path().joinpath(*parts)

def change_ext(path:Path, ext):
    return Path(path.parent).joinpath(path.stem + ext)

