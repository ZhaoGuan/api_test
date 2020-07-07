#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'

import os
import pytest
import allure
import yaml
import subprocess
import shutil
from basics_function.golable_function import config_reader, temp_yml
from basics_function.create_case_yaml import create_case_list
from api_tester.api_tester import ApiTester
from api_tester.testcase_maker import TestCaseMaker

PATH = os.path.dirname(os.path.abspath(__file__))

# create_case_list("all_cases", "dev")
create_case_list("all_cases", "online")
case_data = config_reader(PATH + '/../temp/cases.yaml')
run_data = []
apis = []
run_context_data = []
context_apis = []
for k, v in case_data.items():
    if "context" not in v["path"]:
        run_data.append((v["path"], v["source"]))
        apis.append(v["api"])
    else:
        run_context_data.append((v["path"], v["source"]))
        context_apis.append(v["api"])


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
@pytest.mark.parametrize("path,source", run_data, ids=apis)
def test_template(path, source):
    case = TestCaseMaker(path, source)
    cases = case.case_result()
    if isinstance(cases, dict):
        cases = [cases]
    for _case in cases:
        api_test = ApiTester(_case, source)
        request_api(api_test)
        format_assert(api_test)
        content_assert(api_test)
        anther_assert(api_test)


@pytest.mark.parametrize("path,source", run_context_data, ids=context_apis)
def test_context_template(path, source):
    config_list = config_reader(path)
    temp_result = None
    while config_list:
        step_data = config_list.pop(0)
        if step_data["PATH"] is None:
            temp_path = temp_yml(step_data, PATH + "/../temp_cases/")
        else:
            temp_path = PATH + "/../case" + step_data["PATH"]
        case = TestCaseMaker(temp_path, source)
        case.replace_case_data(step_data)
        api_test = ApiTester(case.case_result(), source)
        api_test.above_response = temp_result
        request_api(api_test)
        format_assert(api_test)
        content_assert(api_test)
        anther_assert(api_test)
        temp_result = api_test.response
    shutil.rmtree(PATH + "/../temp_cases")
