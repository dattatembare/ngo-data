import inspect
import logging
import logging.config as logging_config
from datetime import datetime
from functools import wraps, lru_cache
from time import time
from typing import Any, TypeVar, cast, Callable

from config import env_config
from util import new_log_levels
from util.file_util import get_config
from util.new_log_levels import MyLogger

T = TypeVar('T')


@lru_cache()
def get_logger(obj: Any = 'default') -> MyLogger:
    """
    Creates a logging object and returns it
    :param obj: obj with module, class and method information
    :return: logger object
    """

    name = obj if type(obj) == str else f'{obj.__module__}.{type(obj).__name__}'

    # Get environment specific configs
    config = env_config()

    # Set new log levels
    logging.setLoggerClass(MyLogger)
    logging.addLevelName(new_log_levels.PERF, new_log_levels.PERF_TEXT)
    logging.addLevelName(new_log_levels.TRACE, new_log_levels.TRACE_TEXT)

    # Get logger-config json
    logger_config = get_config(config['logger_config'])

    # Add timestamp to create new file for each new run
    # Updating the filename when {time} is part of filename in logger-config, otherwise log filename will be same
    for k, v in logger_config['handlers'].items():
        if 'filename' in v and '{time}' in v['filename']:
            v['filename'] = v.get('filename').replace('{time}', datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        # Use custom formatter if configured (in config.ini)
        # if 'custom_log' in configs and 'ON' in configs['custom_log'].upper():
        #     v['formatter'] = 'custom'

    logging_config.dictConfig(logger_config)

    # Set custom log levelname
    # if 'custom_log' in config and 'ON' in config['custom_log'].upper():
    #     for loglevel in [new_log_levels.PERF, new_log_levels.TRACE, logging.INFO, logging.INFO, logging.DEBUG,
    #                      logging.WARN, logging.WARNING]:
    #         logging.addLevelName(loglevel, 'DTLOG')
    #
    #     for loglevel in [logging.ERROR, logging.FATAL, logging.CRITICAL]:
    #         logging.addLevelName(loglevel, 'DTERROR')

    logger = logging.getLogger(name)

    if 'log_level' in config and config['log_level'] is not None:
        logger.setLevel(config['log_level'])

    assert isinstance(logger, MyLogger)

    return logger


def trace(orig_func: Callable[..., T]) -> Callable[..., T]:
    """
    A decorator that wraps the passed in function and logs tracing messages
    :param orig_func: original calling function
    :return: wrapper for orig_func
    """
    frm = inspect.stack()[1]  # Calling method absolute file/module path
    logger: MyLogger = get_logger()

    @wraps(orig_func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        logger.trace(f'[{_source_path(frm.filename)}.{orig_func.__name__}()] : '
                     f'START execution with args: {args}, and kwargs: {kwargs}')
        func_result = orig_func(*args, **kwargs)
        logger.trace(f'[{_source_path(frm.filename)}.{orig_func.__name__}()] : END execution')
        return func_result

    return wrapper


def timer(orig_func: Callable[..., T]) -> Callable[..., T]:
    """
    A decorator that wraps the passed in function and logs execution time for that function
    :param orig_func: original calling function
    :return: wrapper for orig_func
    """

    frm = inspect.stack()[1]  # Calling method absolute file/module path
    logger: MyLogger = get_logger()

    @wraps(orig_func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        logger.trace(f'[{_source_path(frm.filename)}.{orig_func.__name__}()] : '
                     f'START execution with args: {args}, and kwargs: {kwargs}')
        start = time()
        func_result = orig_func(*args, **kwargs)
        execution_time = time() - start
        logger.perf(f'[{_source_path(frm.filename)}.{orig_func.__name__}()] : Ran in: {execution_time} sec')
        logger.trace(f'[{_source_path(frm.filename)}.{orig_func.__name__}()] : END execution')
        return cast(T, func_result)

    return wrapper


def exception(orig_func: Callable[..., T]) -> Callable[..., T]:
    """
    A decorator that wraps the passed in function and logs exceptions should one occur
    :param orig_func: original calling function
    :return: wrapper for orig_func
    """

    logger: MyLogger = get_logger()

    @wraps(orig_func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            func_result = orig_func(*args, **kwargs)
        except Exception as e:
            logger.exception(f'{e}')
            raise
        return cast(T, func_result)

    return wrapper


def _source_path(filename: str) -> str:
    """
    method returns source path
    :param filename: source code file name
    :return: source file path from src package
    """

    source_path = filename.replace('.py', '').replace('/', '.').replace('\\', '.')
    if '.test.' in source_path:
        return source_path[source_path.index('.test.') + 1:]
    elif '.test_automation.' in source_path:
        return source_path[source_path.index('.test_automation.') + 1:]
    elif '.src.' in source_path:
        return source_path[source_path.index('.src.') + 1:]
    else:
        return source_path
