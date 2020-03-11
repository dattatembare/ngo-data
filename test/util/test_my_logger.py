import logging
import time
from unittest import TestCase

from testfixtures import LogCapture

from src.util.my_logger import get_logger, trace, exception, timer


class TestLogger(TestCase):
    """
    Run or debug these tests using unit_test_launcher, dir_path is depends on that.
    """

    def test_logger_error(self):
        self.logger = get_logger('error_file_handler')
        self.logger.setLevel(logging.ERROR)

        # pip install testfixtures
        with LogCapture() as l:
            self.use_exception()
            l.check(
                ('error_file_handler', 'ERROR', 'division by zero')
            )

    def test_logger_trace(self):
        self.logger = get_logger()
        self.logger.setLevel(logging.DEBUG)

        with LogCapture() as l:
            self.use_trace()
            l.check(('default',
                     'TRACE',
                     '[test.util.test_my_logger.use_trace()] : START execution with args: '
                     '(<test.util.test_my_logger.TestLogger testMethod=test_logger_trace>,), and '
                     'kwargs: {}'),
                    ('default', 'DEBUG', 'inside use_trace method'),
                    ('default', 'INFO', 'Some execution info'),
                    ('default', 'TRACE', '[test.util.test_my_logger.use_trace()] : END execution'))

    def test_use_timer(self):
        self.logger = get_logger()
        self.logger.setLevel(logging.DEBUG)

        with LogCapture() as l:
            self.use_timer()
            result = l.records
            print(result)
            self.assertEqual('default', result[0].name, 'Test Failed! Invalid logger name')
            self.assertEqual('TRACE', result[0].levelname, 'Test Failed! Invalid level name')
            self.assertEqual('[test.util.test_my_logger.use_timer()] : START execution with args: (<test.util.test_my_logger.TestLogger testMethod=test_use_timer>,), and kwargs: {}',
                             result[0].msg,
                             'Test Failed! Invalid message')

            self.assertEqual('default', result[1].name, 'Test Failed! Invalid logger name')
            self.assertEqual('INFO', result[1].levelname, 'Test Failed! Invalid level name')
            self.assertEqual('Verify time taken by process', result[1].msg, 'Test Failed! Invalid message')

            print(f'Verify timer functionality: {result[2].msg}')
            self.assertEqual('default', result[2].name, 'Test Failed! Invalid logger name')
            self.assertEqual('PERF', result[2].levelname, 'Test Failed! Invalid level name')
            self.assertIn('[test.util.test_my_logger.use_timer()] : Ran in: 5.', result[2].msg,
                          'Test Failed! Invalid message')

            self.assertEqual('default', result[3].name, 'Test Failed! Invalid logger name')
            self.assertEqual('TRACE', result[3].levelname, 'Test Failed! Invalid level name')
            self.assertEqual('[test.util.test_my_logger.use_timer()] : END execution', result[3].msg,
                             'Test Failed! Invalid message')

    @trace
    def use_trace(self):
        logger = get_logger()
        logger.debug(f'inside use_trace method')
        logger.info(f'Some execution info')

    @exception
    def use_exception(self):
        try:
            _result = 10 / 0
        except Exception as e:
            self.logger.exception(f'{e}')

    @timer
    def use_timer(self):
        logger = get_logger()
        logger.info('Verify time taken by process')
        time.sleep(5)
