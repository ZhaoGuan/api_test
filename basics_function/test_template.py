#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'

import os
import pytest
import allure
import shutil
import json
from basics_function.golable_function import config_reader, temp_yml
from api_tester.api_tester import ApiTester
from api_tester.case_maker import CaseMaker, env_data

PATH = os.path.dirname(os.path.abspath(__file__))

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


@pytest.fixture(scope="session")
def result_print(request):
    return request.config.getoption("--result_print")


@allure.step
def request_api(api_test, result_print):
    api_test.api_test()
    if result_print == "true":
        print("请求的url: ", api_test.the_url)
        print("请求的headers: ", api_test.the_headers)
        print("请求体： ", api_test.the_body)
        print("返回状态码", str(api_test.response.status_code))
        try:
            print("返回结果", json.dumps(json.loads(api_test.response.text), sort_keys=True, indent=4, ensure_ascii=False))
        except:
            print("返回结果： ", api_test.response.text)


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
def test_template(path, source, result_print):
    if result_print == "true":
        print("\n用例路径:", path)
    case = CaseMaker(path, source)
    cases = case.case_result()
    if isinstance(cases, dict):
        cases = [cases]
    for _case in cases:
        api_test = ApiTester(_case, source)
        request_api(api_test, result_print)
        format_assert(api_test)
        content_assert(api_test)
        anther_assert(api_test)


@allure.feature("上下文接口测试用例")
@pytest.mark.parametrize("path,source", run_context_data, ids=context_apis)
def test_context_template(path, source, result_print):
    os.mkdir(PATH + "/../temp_cases/")
    if result_print == "true":
        print("\n用例路径:", path)
    config_list = config_reader(path)
    temp_result = None
    env = env_data(path, PATH + "/../env_config/config")
    while config_list:
        step_data = config_list.pop(0)
        if step_data["PATH"] is None:
            step_data["ENV_DATA"] = env
            temp_path = temp_yml(step_data, PATH + "/../temp_cases/")
        else:
            temp_path = PATH + "/../case" + step_data["PATH"]
        case = CaseMaker(temp_path, source)
        case.replace_case_data(step_data)
        api_test = ApiTester(case.case_result(), source)
        api_test.above_response = temp_result
        request_api(api_test, result_print)
        format_assert(api_test)
        content_assert(api_test)
        anther_assert(api_test)
        temp_result = api_test.response
    shutil.rmtree(PATH + "/../temp_cases")
