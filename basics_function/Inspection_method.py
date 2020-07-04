#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Gz"
import requests
import json
import io
from PIL import Image
import random
from basics_function.golable_function import url_parse
from basics_function.golable_function import get_response_content_md5

"""
相关语法的定义:
| 表示或
null 表示 None 关键是这个Json直接就是了
$$$ 表示忽略
"""


def data_content_list_data_case(case):
    case_data = case.split("=")
    replacement = case_data[0].split(">")
    case_value = case_data[1]
    if "%" in case_value:
        check_type = "format"
        check_value = json.loads(case_value.replace("%", ""))
    elif "#" in case_value:
        check_type = "structure"
        check_value = "#"
    else:
        check_type = "equal"
        check_value = case_value
    return {"check_type": check_type, "check_value": check_value, "replacement": replacement}


def response_data_check_other(case, response):
    if (str(case) != str(response) and str(case) != "$$$" and str(case) != "null") or (case == "URL_WRONG") or (
            str(case) == "null" and (response != "null" and response is not None)):
        return False
    else:
        return True


def list_repeated_examination(response, diff=[]):
    new_response = []
    repeated = []
    for i in response:
        if i not in new_response:
            new_response.append(i)
        else:
            repeated.append(i)
    if len(repeated) > 0:
        diff.append(False)
        print("$$$$$$$$$$$$$$$$$$$")
        print("list中有重复内容")
        print("response:" + str(response))
        print("重复的内容为:" + str(repeated))
        print("$$$$$$$$$$$$$$$$$$$$")


def list_empty_check(case, response, diff=[]):
    if len(response) == 0:
        diff.append(False)
        print("$$$$$$$$$$$$$$$$$$$")
        print("response list内容为空:")
        print("case:" + str(case))
        print("response:" + str(response))
        print("$$$$$$$$$$$$$$$$$$$")


class InspectionMethod:
    def __init__(self):
        self.resources_to_test = True
        self.request_time_out = 20
        self.extra = {"LIST_REPEATED": True,
                      "LIST_EMPTY": True,
                      "DICT_LIST_COUNT": None,
                      "URL_FROM": None,
                      "EMPTY_STRING_CHECK": True
                      }
        # host+path 和 url+MD5 判断应该做 配置文件
        self.requests = requests
        self.url_fail = []

    # http资源验证
    def get_pic_size(self, pic):
        img = Image.open(pic)
        size = list(img.size)
        height = size[1]
        width = size[0]
        return {"height": height, "width": width}

    def get_url_stream(self, url):
        url = str(url).replace("%2F", "/")
        if self.extra["URL_FROM"] is not None and self.extra["URL_FROM"] not in url:
            print("资源来源不是" + str(self.extra["URL_FROM"]))
        try:
            response = self.requests.head(url, timeout=self.request_time_out)
            if response.status_code == 200:
                response = self.requests.get(url, timeout=self.request_time_out)
                print(url)
                return io.BytesIO(response.content)
            else:
                print(url)
                print("Http请求错误!")
                print(response.status_code)
                self.url_fail.append(url)
                return False
        except Exception as e:
            print(e)
            print("Http请求错误!")
            self.url_fail.append(url)
            return False

    def http_resource(self, url):
        url = str(url).replace("%2F", "/")
        if self.extra["URL_FROM"] is not None and self.extra["URL_FROM"] not in url:
            print(url)
            print("资源来源不是" + str(self.extra["URL_FROM"]))
        try:
            resources = self.requests.head(url, timeout=self.request_time_out)
            if resources.status_code in [200, 300, 301, 302, 303, 304, 305, 306, 307]:
                return True
            else:
                print("url请求错误" + str(resources.status_code))
                return False
        except Exception as e:
            print(e)
            print("Http请求错误")
            return False

    def response_data_check_url(self, response):
        if self.resources_to_test:
            return self.http_resource(response)
        else:
            return True

    def response_data_check_str(self, response):
        # 判断字符串是否为空字符串
        if ((response != "") and (self.extra["EMPTY_STRING_CHECK"])) or self.extra["EMPTY_STRING_CHECK"] is False:
            return isinstance(response, str)
        else:
            print("出现空字符串")
            return False

    # 返回数据详细校验
    # 检查字段类型 null HTTP Bool Str Int Float 或者 值相等
    def response_data_check_(self, case, response):
        # None处理
        if (case == "Str") and (
                ("http" == str(response)[0:4]) and (str(response[-4:]) != ".com") and (".com" in str(response)) and (
                " " not in str(response))) or case == "HTTP":
            return self.response_data_check_url(response)
        elif case == "Bool":
            return isinstance(response, bool)
        elif case == "Str":
            return self.response_data_check_str(response)
        elif case == "Int":
            return isinstance(response, int)
        elif case == "Float":
            if response == 0.0:
                return True
            else:
                return isinstance(response, float)
        else:
            return response_data_check_other(case, response)

    # 返回数据校验
    # 多个可能有一个可以那么就通过
    def response_data_check(self, case, response):
        result = []
        if "|" in str(case):
            case_ = str(case).split("|")
            for i in case_:
                result.append(self.response_data_check_(i, response))
        else:
            result.append(self.response_data_check_(case, response))
        if True in result:
            return True
        else:
            print(str(result))
            print("返回数据校验错误,错误内容:")
            print("case:" + str(case))
            print("response:" + str(response))
            return False

    def get_key_value_list(self, keys, data):
        for i in keys:
            # 遇到list进行处理
            try:
                i = int(i)
            except Exception as e:
                print(e)
            # 对层级错误进行报错
            try:
                if i == "random":
                    data = data[random.choice(list(range(len(data))))]
                else:
                    data = data[i]
            except Exception as e:
                print(e)
                print("不存在字段，内容报错:")
                print(str(i))
                print(str(data))
                data = False
        return data

    # response字段获取
    def get_key_value(self, keys, data):
        if "/" in str(keys):
            keys = keys.split("/")
        if isinstance(keys, list):
            data = self.get_key_value_list(keys, data)
        else:
            try:
                data = data[keys]
            except Exception as e:
                print(e)
                print("不存在字段，内容报错:")
                print(str(keys))
                print(str(data))
                data = False
        return data

    # key value 条件判断
    """
    case 的格式为k/k/k=v
    """

    def key_value_check(self, case, data):
        case = case.split("=")
        keys = case[0]
        value = case[1]
        data_value = self.get_key_value(keys, data)
        if value == data_value:
            return True
        else:
            return False

    # response检查list类型
    # 默认进行重复检查
    def format_list(self, case, response, diff=[]):
        model = case[0]
        if self.extra["LIST_REPEATED"] is True:
            list_repeated_examination(response=response, diff=diff)
        if self.extra["LIST_EMPTY"] is True:
            list_empty_check(case, response, diff)
        for i in case:
            for e in response:
                if isinstance(i, str):
                    diff.append(self.response_data_check(model, e))
                else:
                    self.format_diff(i, e, diff)

    def dict_key_list_count(self, key, response_list, diff=[]):
        for check_key, check_count in self.extra["DICT_LIST_COUNT"].items():
            if check_key == key and len(response_list) > int(check_count):
                print("$$$$$$$$$$$$$$$$$$$")
                print(key, "对应的list长度为" + str(len(response_list)) + "超过判断长度" + str(check_count))
                print("$$$$$$$$$$$$$$$$$$$")
                diff.append(False)

    def _format_dict(self, case, response, key, diff):
        if isinstance(case[key], list) and isinstance(response[key], list):
            if self.extra["DICT_LIST_COUNT"] is not None:
                self.dict_key_list_count(key, response[key], diff=diff)
            if (isinstance(case[key], dict) and ("$$$" not in case[key])) or (
                    isinstance(case[key], str) and (case[key] != response[key])):
                self.format_diff(case[key], response[key], diff)
            else:
                self.format_list(case[key], response[key], diff)
        elif isinstance(case[key], str):
            # 待验证
            diff.append(self.response_data_check(case[key], response[key]))
        else:
            self.format_diff(case[key], response[key], diff)

    # response检查dict类型
    def format_dict(self, case, response, diff=[]):
        if case.keys() == response.keys():
            for key in case.keys():
                # 值得类型是list进行忽略检查
                self._format_dict(case, response, key, diff)
        else:
            print("错误内容:")
            print("字典型key不匹配")
            print("case: " + str(case.keys()))
            print("response: " + str(response.keys()))
            print("case: " + str(case))
            print("response: " + str(response))
            diff.append(False)

    # response检查格式
    def format_diff(self, case, response, diff=[]):
        try:
            # case为list
            if isinstance(case, list) and isinstance(response, list):
                self.format_list(case, response, diff=diff)
            # case 为dict
            elif isinstance(case, dict):
                self.format_dict(case, response, diff=diff)
            # case 为str
            else:
                if case is None:
                    case = "null"
                if response is None:
                    response = "null"
                diff.append(self.response_data_check(case, response))
        except Exception as e:
            diff.append(False)
            print(e)
            print("错误内容:")
            print("case:" + str(case))
            print("response:" + str(response))
        if False in diff:
            return False
        else:
            return True

    # 检查格式条件判断
    def structure_format_diff(self, case, response):
        try:
            format_type = case["TYPE"]
            format_data = case["DATA"]
        except Exception as e:
            print(e)
            format_type = "ONLY"
            format_data = case
        result_list = []
        diff = []
        if format_type == "ONLY":
            return self.format_diff(format_data, response, diff=diff)
        else:
            # 多个可能时case
            for content, single_case in format_data.items():
                if self.key_value_check(content, response):
                    result_list.append(self.format_diff(single_case, response, diff=diff))
                else:
                    print('未发现对应DATA_FORMAT条件')
                    print('条件为:' + str(content))
        if True in result_list:
            return True
        else:
            return False

    # 条件确认

    # 发现不对就不对了,字典强匹配
    """
        case格式a=1&b=2
        data 为一个字典
        """

    def structure_check(self, structure, data):
        result = True
        truth_structure = structure.split("@")[0]
        case_list = truth_structure.split("&")
        for i in case_list:
            case_ = i.replace("!", "").split("=")
            keys = case_[0].split("/")
            value = case_[1]
            if self.get_key_value(keys, data) != value and value != "#":
                result = False
                break
            elif self.get_key_value(keys, data) != value and value != "#" and "!" in structure:
                break
            # 检查结构不检查值
            elif value == "#":
                result = self.get_key_value(keys, data)
        return result

    # 具体值得检查
    def content_check(self, case_keys, case_value, response):
        response = self.get_key_value(case_keys, response)
        # # 表示检查格式
        # case中因为转换所有都为str,所以强制装换response
        if (case_value == "#" and response is not False) or (response is not False and str(response) == case_value):
            return True
        else:
            return False

    def content_check_unequal(self, case_keys, case_value, response):
        response = self.get_key_value(case_keys, response)
        # # 表示检查格式
        # case中因为转换所有都为str,所以强制装换response
        if (case_value == "#" and response is not False) or (
                response is not False and str(response) != str(case_value)):
            return True
        else:
            return False

    # 单一条件判断
    """
    单一判断判断的值中有/那么会按照一个list去处理
    """

    def multivalued_split_check(self, check_value, structure, response):
        temp = []
        # 循环检查有正确就是正确
        for case_value_ in check_value.split("|"):
            temp.append(self.content_check(structure, case_value_, response))
        if True in temp:
            return True
        else:
            return False

    def multivalued_split_check_unequal(self, check_value, structure, response):
        temp = []
        # 循环检查有正确就是正确
        for case_value_ in check_value.split("|"):
            temp.append(self.content_check_unequal(structure, case_value_, response))
        if True in temp:
            return True
        else:
            return False

    def single_data_content_check_equal(self, case, response):
        case = case.split("=")
        case_value = case[1]
        case_keys = case[0]
        if "|" in case_value:
            return self.multivalued_split_check(case_keys, case_value, response)
        else:
            return self.content_check(case_keys, case_value, response)

    def single_data_content_check_unequal(self, case, response):
        case = case.split("!=")
        case_value = case[1]
        case_keys = case[0]
        if "|" in case_value:
            return self.multivalued_split_check_unequal(case_keys, case_value, response)
        else:
            return self.content_check_unequal(case_keys, case_value, response)

    def single_data_content_check(self, structure, case, data, response):
        try:
            structure_list = self.structure_check(structure, response)
        except Exception as e:
            print(e)
            structure_list = False
        if structure_list or structure == "~all":
            if "!=" in str(case):
                return self.single_data_content_check_unequal(case, response)
            else:
                return self.single_data_content_check_equal(case, response)
        else:
            print("未满足条件:" + structure)
            print("数据内容为:")
            print(str(data))
            return True

    def data_content_list_response_list_split(self, temp, upper_structure, structure, data):
        temp_data = self.get_key_value(structure, data)
        if isinstance(temp_data, list):
            for temp_data_ in temp_data:
                key = temp_data.index(temp_data_)
                this_structure = self.new_structure(upper_structure, structure)
                new_structure = self.new_structure(this_structure, key)
                temp.append({"response_data": temp_data_, "structure": new_structure})
        else:
            new_structure = self.new_structure(upper_structure, structure)
            temp.append({"response_data": temp_data, "structure": new_structure})

    def data_content_list_response_data_analysis(self, structure, data):
        upper_structure = data["structure"]
        response_data = data["response_data"]
        if isinstance(response_data, list) and response_data != []:
            temp = []
            response = []
            for i in response_data:
                key = response_data.index(i)
                this_structure = self.new_structure(upper_structure, key)
                self.data_content_list_response_list_split(temp, this_structure, structure, i)
                response = temp
        elif isinstance(response_data, dict):
            response_data = self.get_key_value(structure, data["response_data"])
            new_structure = self.new_structure(data["structure"], structure)
            response = {"response_data": response_data, "structure": new_structure}
        else:
            response = False
        return response

    def new_structure(self, structure, key):
        return structure + "/" + str(key)

    def data_content_list_response_list_analysis_response_data_list(self, structure, response):
        temp_all = []
        for data in response:
            response = self.data_content_list_response_data_analysis(structure, data)
            if isinstance(response, list):
                print(response)
                for i in response:
                    temp_all.append(i)
            elif isinstance(response, str):
                temp_all.append(response)
        return temp_all

    def data_content_list_response_list_analysis(self, structure, response):
        if "response_data" in str(response):
            if isinstance(response, list):
                response = self.data_content_list_response_list_analysis_response_data_list(structure, response)
            else:
                response = self.data_content_list_response_data_analysis(structure, response)
        elif isinstance(response, list) or isinstance(response, dict):
            response_data = self.get_key_value(structure, response)
            response = {"response_data": response_data, "structure": structure}
        else:
            response = False
        return response

    def data_content_list_response_data(self, structure_list, response):
        for structure in structure_list:
            response = self.data_content_list_response_list_analysis(structure, response)
        return response

    def data_content_list_data_structure(self, structure, response):
        value = structure.split("=")[1]
        structure_list = structure.split("=")[0].split("//")
        structure_result = []
        try:
            data = self.data_content_list_response_data(structure_list, response)
            if data is False:
                return False
        except Exception as e:
            print("条件层级解析错误")
            print(e)
            print(str(structure))
            return False
        for i in data:
            response_data = i["response_data"]
            structure = i["structure"]
            if response_data == value:
                structure_result.append(structure)
        return structure_result

    def data_content_list_check(self, structure_result, case_data, response):
        replacement = case_data["replacement"]
        check_type = case_data["check_type"]
        check_value = case_data["check_value"]
        result_list = []
        for structure in structure_result:
            structure = structure.replace(replacement[0], replacement[1])
            check_response = self.get_key_value(structure, response)
            if check_type == "format":
                result_list.append(self.structure_format_diff(check_value, check_response))
            elif "|" in check_value:
                result = self.multivalued_split_check(check_value, structure, response)
                result_list.append(result)
            else:
                response_value = self.get_key_value(structure, response)
                if ("check_value" == check_value and response_value == check_value) or (response_value is not False):
                    result_list.append(True)
                else:
                    result_list.append(False)
        if False in result_list:
            return False
        else:
            return True

    # 具体数据的判断 有判断没有不判断
    def data_content_check(self, case, data, response):
        result_list = []
        for structure, case_ in case.items():
            if "//" in str(structure):
                structure_result = self.data_content_list_data_structure(structure, response)
                if structure_result is not False:
                    case_data = data_content_list_data_case(case_)
                    result_list.append(self.data_content_list_check(structure_result, case_data, response))
            else:
                result_list.append(self.single_data_content_check(structure, case_, data, response))
        if False in result_list:
            return False
        else:
            return True

    def header_check_(self, case, value, response_header):
        response_header_value = self.get_key_value(case, response_header)
        if "|" in value and response_header_value is not False:
            if response_header[case] in list(value.split("|")):
                return True
            else:
                return False
        elif response_header_value is not False:
            if response_header[case] == value:
                return True
            else:
                return False
        else:
            return False

    def header_check(self, case, response_header):
        for key, value in case.items():
            if key != "~all":
                if isinstance(value, dict) and self.structure_check(key, response_header):
                    return self.header_check_(list(value.keys())[0], list(value.values())[0], response_header)
                elif isinstance(value, str):
                    return self.header_check_(key, value, response_header)
                else:
                    return False
            else:
                if isinstance(value, dict):
                    return self.header_check_(list(value.keys())[0], list(value.values())[0], response_header)
                elif isinstance(value, str):
                    return self.header_check_(key, value, response_header)
                else:
                    return False
