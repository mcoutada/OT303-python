import os
import pandas as pd

from config import ROOT_TXT


def get_filename_path(src):
    """Get filename and src_path from querys.
    Args:
        src (str): Directory to take filepath and filename.
    Returns:
        Dict{}: key: filename of SQL querys, value: full path.
    """
    files_path = {}
    for name in os.listdir(src):
        files_path[name] = os.path.join(src, name)
    return files_path


def create_folder(path):
    """Create folder if doesnt exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def create_txt(df: pd.DataFrame, file_name: str):
    """Create file.txt from pandas dataframe and return the file.
    Args:
        df (pd.DataFrame): Dataframe.
        file_name (str): Filename.
    Returns:
        text_file: text_file generated.
    """
    path = os.path.join(ROOT_TXT, file_name+'.txt')
    text_file = df.to_csv(path, index=False)

    return text_file