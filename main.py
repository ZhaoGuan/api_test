#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from basics_function.json_to_format_case import data_clear
import sys, getopt
import os
import yaml
import pytest
from record_to_case.har_to_case import HarToCase
from basics_function.create_case_yaml import create_case_list, add_case
from basics_function.json_to_format_case import data_clear

msg = '''
-h --help 
-r --record main.py 指定读取.har文件路径进行用例转换
-p --path .har文件录制转换结果路径,使用-s可以设置source不然默认为online
-c --cases 运行case某个文件夹的用例，all_case时为所有文件夹
-f --filepath 运行用例文件夹下某一个用例case文件夹的相对路径
-s --source 运行case所指定的环境,不填写默认为online
-j --json json内容转化为format校验内容
    eg: -j '{"a":1}'
-a --alluredir pytest allure报告数据格式存放文件夹，默认为./report
-z --result_print 是否在命令行中打印请求内容和结果 true false
'''

PATH = os.path.dirname(os.path.abspath(__file__))


def opt_check(opts):
    is_record = False
    record_path = PATH + "/case/"
    cases = False
    source = "online"
    json_data = False
    filepath = False
    alluredir = "./report"
    result_print = 'false'
    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            print(msg)
            exit()
        if opt in ["-r", "--record"]:
            is_record = arg
        if opt in ["-p", "--path"]:
            record_path = arg
        if opt in ["-c", "-case"]:
            cases = arg
        if opt in ["-s", "--source"]:
            source = arg
        if opt in ["-j", "--json"]:
            json_data = arg
        if opt in ["-f", "--filepath"]:
            filepath = arg
        if opt in ["-a", "--alluredir"]:
            alluredir = arg
        if opt in ["-z", "--result_print"]:
            result_print = arg
    return is_record, record_path, cases, source, json_data, filepath, alluredir, result_print


def har_to_case(is_record, record_path, source):
    try:
        htc = HarToCase(is_record, source)
        htc.to_case(record_path)
    except Exception as e:
        print("ERROR:")
        print(e)


def run_cases(cases, source, alluredir, result_print):
    try:
        create_case_list(cases, source)
        pytest.main(["-s", "-q", "--alluredir", alluredir, "--result_print", result_print])
    except Exception as e:
        print("ERROR:")
        print(e)


def single_case(filepath, source, alluredir, result_print):
    try:
        data = add_case(filepath, source)
        with open(PATH + "/temp/cases.yaml", "w") as f:
            yaml.dump(data, f, default_flow_style=False)
        pytest.main(["-s", "-q", "--alluredir", alluredir, "--result_print", result_print])
    except Exception as e:
        print("ERROR:")
        print(e)


def json_to_format_case(json_data):
    try:
        print(data_clear(json_data))
    except Exception as e:
        print("ERROR:")
        print(e)


def run(argv):
    try:
        opts, args = getopt.getopt(argv, '-h-z:-r:-p:-c:-f:-s:-j:-a:',
                                   ["--help", "--record", "--path", "--source", "--cases", "--filepath", "--json",
                                    "result_print"])
    except getopt.GetoptError:
        print(msg)
        exit()
    is_record, record_path, cases, source, json_data, filepath, alluredir, result_print = opt_check(opts)
    if is_record:
        har_to_case(is_record, record_path, source)
    if cases:
        run_cases(cases, source, alluredir, result_print)
    if filepath:
        single_case(filepath, source, alluredir, result_print)
    if json_data:
        json_to_format_case(json_data)


if __name__ == '__main__':
    run(sys.argv[1:])
