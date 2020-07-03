#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import os
import json
import base64
import yaml


# 根据数据类型生成校验参数
def data_type_case(data):
    if isinstance(data, str) and "http" in data:
        data_type = "HTTP"
    elif isinstance(data, bool) or data == "bool":
        data_type = "Bool"
    elif isinstance(data, str) or data == "string":
        data_type = "Str"
    elif isinstance(data, int) or data == "int":
        data_type = "Int"
    elif isinstance(data, float) or data == "float":
        data_type = "Float"
    else:
        # 处理了None
        data_type = None
    return data_type


# content数据清洗
# 把接口中的值清理了
# 如果遇到的是一个LIST那么默认其中所有的内容都是一致的只保留一个模板内容
def ergodic_list(data):
    if len(data) > 0:
        for i in range(len(data)):
            if i == 0:
                if isinstance(data[i], str) or isinstance(data[i], int) or \
                        isinstance(data[i], bool) or isinstance(data[i], float) or data[i] is None:
                    data[i] = data_type_case(data[i])
                    print("list中存放的不是dict")
                else:
                    ergodic(data[i])
            else:
                data[i] = "####"
    else:
        # 对空list的忽略
        data.append("$$$")


def ergodic_dict(data):
    for key in data.keys():
        if isinstance(data[key], str) or isinstance(data[key], int) or \
                isinstance(data[key], bool) or isinstance(data[key], float) or data[key] is None:
            data[key] = data_type_case(data[key])
        else:
            ergodic(data[key])


def ergodic(data):
    if isinstance(data, list):
        ergodic_list(data)
    elif isinstance(data, dict):
        ergodic_dict(data)
    return data


def delete_none(data):
    for k, v in data.items():
        if isinstance(v, list):
            data[k] = [v[0]]
            print(data[k])
        if isinstance(v, dict):
            delete_none(v)


# 异常数据处理
# 需要根据具体情况添加主要解决不识别问题
def data_clear(data):
    if isinstance(data, bytes):
        data = data.decode("utf-8")
    data = json.loads(data)
    data = ergodic(data)
    data = json.loads(json.dumps(data).replace(', "####"', ""))
    print()
    return data


class HarToCase:
    def __init__(self, path):
        self.path = path

    def get_params(self, params):
        the_params = {}
        if params == []:
            the_params = None
        else:
            for params_data in params:
                the_params[params_data["name"]] = params_data["value"]
        return the_params

    def get_headers(self, headers):
        the_header = {}
        for header_data in headers:
            the_header[header_data["name"]] = header_data["value"]
        return the_header

    def get_post(self, request):
        request_mimetype = request["postData"]["mimeType"]
        post_body = request["postData"]["params"]
        the_post_body = {}
        if request_mimetype == "application/x-www-form-urlencoded":
            for response_body_data in post_body:
                the_post_body[response_body_data["name"]] = response_body_data["value"]
            request_post_type = "NORMAL"
            body_type = "JSON"
            request_body_function = "NORMAL"
        if the_post_body == {}:
            the_post_body = None
        return the_post_body, request_post_type, body_type, request_body_function

    def to_case(self, case_path):
        with open(self.path, "r") as f:
            har_data = json.load(f)
        http_data = har_data["log"]["entries"]
        for data in http_data:
            # request things
            request = data["request"]
            method = request['method']
            url = request["url"]
            headers = request["headers"]
            the_header = self.get_headers(headers)
            params = request["queryString"]
            the_params = self.get_params(params)
            the_post_body, request_post_type, body_type, request_body_function = self.get_post(request)
            # response things
            response = data["response"]
            content = response["content"]
            response_mimetype = content["mimeType"]
            response_body = content["text"]
            encoding = content["encoding"]
            if response_mimetype == "application/json;charset=UTF-8" and encoding == "base64":
                response_body = base64.b64decode(response_body).decode('utf-8')
            case_data = {'OPERATION_MODE': 'single', 'SOURCE': {
                'online': {'URL': url,
                           'HEADERS': {'TYPE': 'NORMAL', 'DATA': the_header},
                           'PARAMS': {'TYPE': 'JOIN', 'DATA': the_params},
                           'MODE': {'TYPE': method}, 'BODY': {'TYPE': body_type, 'DATA': the_post_body}}},
                         'DATA_FORMAT': {"DATA": data_clear(response_body), "TYPE": "ONLY"}, 'DATA_CONTENT': None,
                         'RESPONSE_HEADER': None}
            file_name = url.split("/")[-1] + ".yml"
            with open(case_path + "/" + file_name, "w") as f:
                yaml.dump(case_data, f)


if __name__ == "__main__":
    htc = HarToCase("./Desktop.har")
    htc.to_case("./")
