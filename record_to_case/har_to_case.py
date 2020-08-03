#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import os
import json
import base64
import yaml
from basics_function.json_to_format_case import data_clear


class HarToCase:
    def __init__(self, path, source):
        self.path = path
        self.source = source

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
        try:
            request_mimetype = request["postData"]["mimeType"]
        except:
            request_mimetype = None
        try:
            post_body = request["postData"]["params"]
        except:
            post_body = None
        the_post_body = {}
        if request_mimetype is not None and "application/x-www-form-urlencoded" in request_mimetype:
            for response_body_data in post_body:
                the_post_body[response_body_data["name"]] = response_body_data["value"]
        request_post_type = "NORMAL"
        body_type = "JSON"
        request_body_function = "NORMAL"
        if the_post_body == {}:
            the_post_body = None
        return the_post_body, request_post_type, body_type, request_body_function

    def new_header(self, header):
        result = {}
        for k, v in header.items():
            if ":" in k:
                continue
            result[k] = v
        return result

    def to_case(self, case_path):
        with open(self.path, "r") as f:
            har_data = json.load(f)
        http_data = har_data["log"]["entries"]
        for data in http_data:
            # request things
            request = data["request"]
            method = request['method']
            url = request["url"].split("?")[0]
            headers = request["headers"]
            the_header = self.get_headers(headers)
            the_header = self.new_header(the_header)
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
            case_data = {'SOURCE': {'URL_PATH': None, 'METHOD': method,
                                    'DATA_TYPE': 'ONLY',
                                    self.source: {'URL': url, 'HEADERS': {'TYPE': 'NORMAL', 'DATA': the_header},
                                                  'PARAMS': {'TYPE': 'JOIN', 'DATA': the_params},
                                                  'BODY': {'TYPE': body_type, 'DATA': the_post_body}}},
                         'ASSERT': {'DATA_FORMAT': {'TYPE': 'ONLY', 'DATA': data_clear(response_body)},
                                    'DATA_CONTENT': None, 'RESPONSE_HEADER': None}}
            file_name = url.split("/")[-1] + ".yml"
            with open(case_path + "/" + file_name, "w") as f:
                yaml.dump(case_data, f)
