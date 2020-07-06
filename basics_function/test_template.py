#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'

import os
import pytest
import allure
import subprocess
from basics_function.golable_function import config_reader, config_data_path
from basics_function.create_case_yaml import create_case_list
from api_tester.api_tester import ApiTester, single_api_tester
from api_tester.testcase_maker import TestCaseMaker

PATH = os.path.dirname(os.path.abspath(__file__))

create_case_list("all_cases")
case_data = config_reader(PATH + '/../temp/cases.yaml')
run_data = []
for k, v in case_data.items():
    run_data.append((v["path"], v["source"]))


@allure.step
def request_api(api_test):
    api_test.api_test()


@allure.step
def format_assert(api_test):
    api_test.format_assert()


@allure.step
def content_assert(api_test):
    api_test.content_assert()


@allure.step
def anther_assert(api_test):
    api_test.another_assert()
    api_test.another_assert_report()


@allure.feature("接口测试用例")
@pytest.mark.parametrize("path,source", run_data)
def test_template(path, source):
    case = TestCaseMaker(path, source)
    api_test = ApiTester(case.case_result(), source)
    request_api(api_test)
    format_assert(api_test)
    content_assert(api_test)
    anther_assert(api_test)
