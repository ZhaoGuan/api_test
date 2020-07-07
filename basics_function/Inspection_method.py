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


class InspectionMethod:
    def __init__(self):
        self.resources_to_test = True
        self.request_time_out = 20
        self.extra = {"LIST_REPEATED": True,
                      "LIST_EMPTY": True,
                      "DICT_LIST_COUNT": None,
                      "URL_FROM": None,
                      "EMPTY_STRING_CHECK": False
                      }
        # host+path 和 url+MD5 判断应该做 配置文件
        self.requests = requests
        self.url_fail = []
        self.fail_list = []

    def fail_append(self, data):
        if data is not None:
            self.fail_list.append(data)

    def response_data_check_other(self, case, response):
        if (str(case) != str(response) and str(case) != "$$$" and str(case) != "null") or (case == "URL_WRONG") or (
                str(case) == "null" and (response != "null" and response is not None)):
            return False
        else:
            return True

    def list_repeated_examination(self, response):
        new_response = []
        repeated = []
        for i in response:
            if i not in new_response:
                new_response.append(i)
            else:
                repeated.append(i)
        if len(repeated) > 0:
            fail_data = {"reason": "\nlist中有重复的内容，重复内容为:{}".format(repeated), "response": response, "case": None}
            self.fail_list.append(fail_data)

    def list_empty_check(self, case, response):
        if len(response) == 0:
            fail_data = {"reason": "\nresponse list内容为空", "response": response, "case": case}
            self.fail_list.append(fail_data)

    # http资源验证
    def http_resource(self, url):
        url = str(url).replace("%2F", "/")
        if self.extra["URL_FROM"] is not None and self.extra["URL_FROM"] not in url:
            self.fail_list.append(
                {"reason": "\n" + url + " 资源来源不是" + str(self.extra["URL_FROM"]), "case": None, "response": None})
        try:
            resources = self.requests.head(url, timeout=self.request_time_out)
            if resources.status_code in [200, 300, 301, 302, 303, 304, 305, 306, 307]:
                return True
            else:
                self.fail_list.append(
                    {"reason": url + "\nurl请求错误" + str(resources.status_code), "case": None, "response": None})
                return False
        except Exception as e:
            print(e)
            self.fail_list.append(
                {"reason": "\nHttp请求错误,错误信息:" + e, "case": None, "response": None})
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
            self.fail_list.append({"reason": "\n出现空字符串", "case": None, "response": response})
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
            return self.response_data_check_other(case, response)

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
            return None
        else:
            return {"reason": "\n返回数据校验错误，错误内容:", "case": str(case), "response": str(response)}

    def get_key_value_list(self, keys, data):
        for i in keys:
            # 遇到list进行处理
            try:
                i = int(i)
            except Exception as e:
                # print(e)
                pass
            # 对层级错误进行报错
            try:
                if i == "random":
                    data = data[random.choice(list(range(len(data))))]
                else:
                    data = data[i]
            except Exception as e:
                self.fail_list.append(
                    {"reason": "\n不存在字段，内容报错:" + str(e), "case": str(keys) + " " + str(data),
                     "response": json.dumps(data)})
                return False
        return data

    # response字段获取
    def get_key_value(self, keys, data):
        if isinstance(keys, list):
            data = self.get_key_value_list(keys, data)
            if data is False:
                return False
        else:
            try:
                data = data[keys]
            except Exception as e:
                self.fail_list.append(
                    {"reason": "\n不存在字段，内容报错:" + str(e), "case": str(keys), "response": json.dumps(data)})
                data = False
        if isinstance(data, int):
            return str(data)
        return data

    # key value 条件判断
    """
    case 的格式为k/k/k=v
    """

    def key_value_check(self, case, data):
        if isinstance(case, dict):
            keys = str(list(case.keys())[0]).split("/")
            value = str(list(case.values())[0]).split("|")
            data_value = self.get_key_value(keys, data)
            if data_value and data_value not in value:
                fail_data = {"reason": "检查字段值与预期不符", "case": case, "response": data}
                self.fail_list.append(fail_data)
                return False
            else:
                return True
        else:
            case = case.split("=")
            keys = str(case[0]).split("/")
            value = str(case[1]).split("|")
            data_value = self.get_key_value(keys, data)
            if data_value and data_value not in value:
                fail_data = {"reason": "检查字段值与预期不符", "case": case, "response": data}
                self.fail_list.append(fail_data)
                return False
            else:
                return True

    # response检查list类型
    # 默认进行重复检查
    def format_list(self, case, response):
        model = case[0]
        if self.extra["LIST_REPEATED"] is True:
            self.list_repeated_examination(response=response)
        if self.extra["LIST_EMPTY"] is True:
            self.list_empty_check(case, response)
        for i in case:
            for e in response:
                if isinstance(i, str):
                    fail_data = self.response_data_check(model, e)
                    self.fail_append(fail_data)
                else:
                    self.format_diff(i, e)

    def dict_key_list_count(self, key, response_list):
        for check_key, check_count in self.extra["DICT_LIST_COUNT"].items():
            if check_key == key and len(response_list) > int(check_count):
                fail_data = {
                    "reason": "\n" + str(key) + " 对应的list长度为" + str(len(response_list)) + "超过判断长度" + str(check_count),
                    "case": None, "response": None}
                self.fail_list.append(fail_data)

    def _format_dict(self, case, response, key):
        if isinstance(case[key], list) and isinstance(response[key], list):
            if self.extra["DICT_LIST_COUNT"] is not None:
                self.dict_key_list_count(key, response[key])
            if (isinstance(case[key], dict) and ("$$$" not in case[key])) or (
                    isinstance(case[key], str) and (case[key] != response[key])):
                self.format_diff(case[key], response[key])
            else:
                self.format_list(case[key], response[key])
        elif isinstance(case[key], str):
            # 待验证
            self.fail_append(self.response_data_check(case[key], response[key]))
        else:
            self.format_diff(case[key], response[key])

    # response检查dict类型
    def format_dict(self, case, response):
        if case.keys() == response.keys():
            for key in case.keys():
                # 值得类型是list进行忽略检查
                self._format_dict(case, response, key)
        else:
            msg = "\nresponse检查dict类型错误,字典型key不匹配\n" \
                  "case: {} \n" \
                  "response: {} \n".format(str(case.keys()), str(response.keys()))
            fail_data = {"reason": msg, "case": case, "response": response}
            self.fail_list.append(fail_data)

    # response检查格式
    def format_diff(self, case, response):
        try:
            # case为list
            if isinstance(case, list) and isinstance(response, list):
                self.format_list(case, response)
            # case 为dict
            elif isinstance(case, dict):
                self.format_dict(case, response)
            # case 为str
            else:
                if case is None:
                    case = "null"
                if response is None:
                    response = "null"
                self.fail_append(self.response_data_check(case, response))
        except Exception as e:
            # print(e)
            fail_data = {"reason": "response格式检查错误", "case": case, "response": response}
            self.fail_list.append(fail_data)
        if len(self.fail_list) > 0:
            return False
        else:
            return True

    # 检查格式条件判断
    def structure_format_diff(self, case, response, json_check=True):
        try:
            if json_check == True:
                response = json.loads(response.text)
        except:
            assert False, "Json解析错误\n" + "数据内容为:{}\n".format(response.text)
        try:
            format_type = case["TYPE"]
            format_data = case["DATA"]
        except Exception as e:
            format_type = "ONLY"
            format_data = case
        result_list = []
        if format_type == "ONLY":
            return self.format_diff(format_data, response)
        else:
            # 多个可能时case
            '''
            DATA:
             k/k/k=v0 : you_data_format_v2
             k/k/k=v1 : you_data_format_v1
            '''
            for content, single_case in format_data.items():
                if self.key_value_check(content, response):
                    result_list.append(self.format_diff(single_case, response))
                else:
                    assert False, "未发现对应DATA_FORMAT条件,条件为: {}".format(str(content))
        if True in result_list:
            return True
        else:
            return False

    def fail_list_assert(self):
        msg = ""
        if len(self.fail_list) > 0:
            for fail in self.fail_list:
                msg = msg + "\n\t错误原因:{}\n\t".format(fail["reason"])
                if fail["case"] is not None:
                    msg = msg + "\n\tcase:{}\n\t".format(fail["case"])
                if fail["response"] is not None:
                    msg = msg + "\n\tresponse:{}\n\t".format(json.dumps(fail["response"]))
                msg = msg + "\n\t"
            assert False, msg

    # data content check
    def specific_value_check(self, case, response):
        case_key = list(case.keys())[0]
        case_value = list(case.values())[0]
        if "=" in case_key:
            if self.key_value_check(case_key, response) and self.key_value_check(case_value, response):
                return True
            else:
                return False
        else:
            return self.key_value_check(case, response)

    def content_structure_check(self, case, response):
        base = list(case.keys())[0]
        to_check_content = list(case.values())[0]
        if self.key_value_check(base, response):
            the_response_keys = str(list(to_check_content.keys())[0]).split("/")
            the_content = list(to_check_content.values())[0]
            the_response = self.get_key_value(the_response_keys, response)
            self.structure_format_diff(the_content, the_response, json_check=False)
        else:
            fail_data = {"reason": "未发现匹配条件", "case": case, "response": response}
            self.fail_list.append(fail_data)

    def _response_content_check(self, case, response):
        case_tag = list(case.keys())[0]
        if case_tag == "STRUCTURE":
            self.content_structure_check(case["STRUCTURE"], response)
        else:
            self.specific_value_check(case, response)

    def response_content_check(self, case, response):
        try:
            response = json.loads(response.text)
        except:
            assert False, "Json解析错误\n" + "数据内容为:{}\n".format(response.text)
        if isinstance(case, list):
            for _case in case:
                self._response_content_check(_case, response)
        else:
            self._response_content_check(case, response)
        if len(self.fail_list) > 0:
            return False
        else:
            return True
