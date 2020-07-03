#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Gz"
import yaml
import os

PATH = os.path.dirname(os.path.abspath(__file__))


def dirlist(path, allfile):
    file_list = os.listdir(path)
    for filename in file_list:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            dirlist(filepath, allfile)
        else:
            allfile.append(filepath)
    return allfile


def select_case_folder(options):
    if options == "all_cases":
        result = []
        path = PATH + "/../case"
        return dirlist(path, result)
    else:
        return case_list(options)


def case_list(folder_name):
    folder_path = PATH + "/../case/" + folder_name
    folder_list = []
    try:
        dirlist(folder_path, folder_list)
    except Exception as e:
        print(e)
        print("文件夹填写错误")
        assert False
    result = [folder for folder in folder_list]
    return result


def add_case(case, source, temp_server, resources_to_test):
    case_result = {}
    # temp_server 中网站相关的判断属于临时处理 web 地址的暂时不进行测试"
    if ("!" not in case) and ("content" not in case) and (".DS_Store" not in case) and (
            (temp_server is True and ("web" not in case)) or temp_server is False):
        case_result.update({case: {"path": case, "source": source, "temp_server": temp_server,
                                   "resources_to_test": resources_to_test}})
        return {
            case: {"path": case, "source": source, "temp_server": temp_server, "resources_to_test": resources_to_test}}
    else:
        return {}


def create_case_list(folder_name, source="online", temp_server=False, resources_to_test=True):
    case_result = {}
    case_list_data = select_case_folder(folder_name)
    for case in case_list_data:
        if ((folder_name == "all_cases") and ("_all_" not in case)) or (folder_name != "all_cases"):
            case_result.update(add_case(case, source, temp_server, resources_to_test))
    if os.path.exists(PATH + "/../temp/") is False:
        os.mkdir(PATH + "/../temp/")
    with open(PATH + "/../temp/cases.yaml", "w") as case:
        yaml.dump(case_result, case, default_flow_style=False)
