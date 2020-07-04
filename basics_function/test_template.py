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
    api_test.api_assert()


@allure.feature("接口测试用例")
@pytest.mark.parametrize("path,source", run_data)
def test_template(path, source):
    config = config_data_path(path)
    api_test = ApiTester(config, source)
    request_api(api_test)
    format_api(api_test)
