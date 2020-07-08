#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from basics_function.HTMLTestRunner import HTMLTestRunner
from basics_function.golable_function import config_reader
from ddt import ddt, data, file_data, unpack
from api_tester.api_tester import single_api_tester
import os
import unittest
import subprocess

PATH = os.path.dirname(os.path.abspath(__file__))


@ddt
class ApiTest(unittest.TestCase):
    def setUp(self):
        print('Test Begin')

    @file_data(PATH + '/../temp/cases.yaml')
    @unpack
    def test_http_api(self, path, source, resources_to_test, temp_server):
        file_path = path
        try:
            run_way = config_reader(file_path)['OPERATION_MODE']
        except:
            run_way = 'py'
        if run_way == 'single':
            result = single_api_tester(path, source)
            assert result
        elif run_way == 'content':
            assert False
        else:
            p = subprocess.Popen('python3 ' + file_path + ' -s ' + source, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
            result = str(p.stdout.read().decode())
            if ('失败' in result) or ('AssertionError' in result) or ('Traceback' in result) or ('SyntaxError' in result):
                assert False

    def tearDown(self):
        print('Test Over')


def case_runner():
    # 编辑用例
    # unittest.main()
    ApiTest()
    suite = unittest.TestSuite()
    # DDT的坑
    discover = unittest.defaultTestLoader.discover(PATH, pattern='running_template.py', top_level_dir=None)
    for test_suit in discover:
        for case in test_suit:
            suite.addTest(case)
    # 执行用例
    # runner = unittest.TextTestRunner()
    filename = PATH + '/../report/Api_test_report.html'
    try:
        os.mkdir(PATH + '/../report')
    except:
        pass
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp, title='接口自动化测试报告', description='接口自动化测试报告')
    runner.run(suite)
    fp.close()


if __name__ == "__main__":
    case_runner()
