import argparse
import importlib
import os
import unittest
from unittest import TextTestRunner

from HtmlTestRunner import HTMLTestRunner

from src.util.file_util import dir_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-r',
        '--report_type',
        help='The profile name',
        required=False,
        default='text'
    )

    args = parser.parse_args()
    report_type = args.report_type.lower()

    process_dir(dir_path(__file__), 'test')
    all_my_base_classes = [unittest.defaultTestLoader.loadTestsFromTestCase(cls) for cls in
                           unittest.TestCase.__subclasses__() if cls.__module__.startswith('test.')]
    suite = unittest.TestSuite(all_my_base_classes)

    if report_type == 'text':
        # Text Test Report:
        # verbosity=2 unittest will print the result of each test run.
        TextTestRunner(verbosity=2).run(suite)
    else:
        """
        HTML Test Report:
        Use of HTMLTestRunner need installation.
        Install command: $ pip install html-testRunner
        """
        HTMLTestRunner(
            combine_reports=True,
            report_name='test_report',
            add_timestamp=True,
            open_in_browser=True
        ).run(suite)


def process_dir(path, prefix):
    path, dirs, files = list(os.walk(path))[0]
    for file in files:
        if file.endswith('.py') and not file == __file__:
            importlib.import_module(f'{prefix}.{file.replace(".py", "")}')
    for _dir in dirs:
        process_dir(f'{path}/{_dir}', f'{prefix}.{_dir}')


"""
How to run unit_test_launcher: 
    1. Pycharm/IntelliJ - "Run unit_test_launcher using arrow at line #63 " 
    2. Command line - <root-dir>/logging_n_decorators>python -m test.unit_test_launcher -r html
       Default report type for performance test is 'text'
"""
if __name__ == '__main__':
    main()
