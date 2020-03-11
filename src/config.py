from configparser import ConfigParser
from functools import lru_cache
from os.path import join
from typing import Any, Dict

from util.file_util import project_root_dir

CONFIG_FILE = 'configs/config.ini'
LOCAL_CONFIG_FILE = 'configs/local.ini'


@lru_cache()
def env_config() -> Dict[str, Any]:
    """
    Read config from configs/config.ini or configs/local.ini and return Config object
    :return: Config dict
    """

    # Get environment variable MDPF_ENV which is set in System Environment variables.
    env = 'NGO_DATA'  # os.environ.get('NGO_DATA')
    env = env.upper() if env is not None else ''

    config = ConfigParser()
    if 'LOCAL' == env:
        config.read(join(project_root_dir(), LOCAL_CONFIG_FILE))
    else:
        config.read(join(project_root_dir(), CONFIG_FILE))

    if env in config.sections():
        return {option: config.get(env, option) for option in config.options(env)}
    else:
        raise Exception(f'Invalid env type or NGO_DATA not set in System Environment Variables: {env}')
