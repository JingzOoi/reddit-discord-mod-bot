import os


def blockify(text: str) -> str:
    return f"```{text}```"


def construct_path(*args) -> str:
    path_name = ""
    for a in args:
        path_name = os.path.join(path_name, a)
    return path_name
