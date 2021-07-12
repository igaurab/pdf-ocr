import os
from loguru import logger


def basedir_exists(path) -> bool:
    """
    Checks whether the base directory exists.

    Args:
        path: str
            '/home/user/folder/image.jpg'

    Returns
        bool

    Eg: If '/home/user/folder/' dir exists, returns True else False
    """
    path_dir = os.path.dirname(path)
    path_exists = os.path.exists(path_dir)

    return path_exists


def get_files_from_dir(dir_path):
    logger.info(dir_path)
    file_paths = []
    for dir, _, files in os.walk(dir_path):
        for f in files:
            file_path = os.path.abspath(os.path.join(dir, f))
            file_paths.append(file_path)
    return file_paths


def get_filename(file: str) -> str:
    return os.path.basename(file).split(".")[0]
