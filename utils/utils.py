import os
from config.cfg import ROOT_SQL


def get_src_querys():
    """Get filename and src_path from querys.

    Returns:
        Dict{}: key: filename of SQL querys, value: full path.
    """
    files_path = {}
    for name in os.listdir(ROOT_SQL):
        files_path[name] = os.path.join(ROOT_SQL, name)
    return files_path


def create_folder(path):
    """Create folder if doesnt exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)
