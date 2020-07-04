#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'

import os
import pytest
import allure
import subprocess
from basics_function.golable_function import config_reader, config_data_path
from api_tester.api_tester import ApiTester, single_api_tester

PATH = os.path.dirname(os.path.abspath(__file__))

case_data = config_reader(PATH + '/../temp/cases.yaml')
run_data = []
for k, v in case_data.items():
    run_data.append((v["path"], v["source"]))


def request_api(path, source):
    file_path = path
    try:
        run_way = config_reader(file_path)['OPERATION_MODE']
    except Exception as e:
        print(e)
        run_way = 'py'
    if run_way == 'single':
        result = single_api_tester(path, source)
    elif run_way == 'content':
        result = False
    else:
        p = subprocess.Popen('python3 ' + file_path + ' -s ' + source, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        result = str(p.stdout.read().decode())
    return run_way, result


@allure.feature("接口测试用例")
@pytest.mark.parametrize("path,source", run_data)
def test_template(path, source):
    request_api(path, source)
