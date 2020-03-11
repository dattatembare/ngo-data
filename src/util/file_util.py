import json
from functools import lru_cache
from os.path import dirname, join
from typing import Dict, Any


@lru_cache()
def get_config(config_file: str) -> Dict[str, Any]:
    """
    Returns the logging config dict
    :param config_file: The name of the config file
    :return: The dictionary to use for initializing the logging
    """

    try:
        file_path = join(project_root_dir(), config_file)
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise Exception('9000_UNEXPECTED_ERROR', e) from None


def project_root_dir() -> str:
    """
    method returns project root directory
    :return: project root directory
    """
    return dir_path(__file__, 3)


def dir_path(file_dir: str, depth: int = 1) -> str:
    """
    method returns directory path for provided
    :param file_dir: file path
    :param depth: desired directory depth
    :return: directory path for desired depth
    """
    for cnt in range(depth):
        file_dir = dirname(file_dir)
    return file_dir
