#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from basics_function.golable_function import config_reader, assert_function_import, header_function_import, \
    body_function_import
from basics_function.Inspection_method import InspectionMethod
from urllib.parse import urlencode
import json
import requests


class ApiTester:
    def __init__(self, config, source="online"):
        self.inspection_method = InspectionMethod()
        self.case_data = config
        try:
            self.env_data = self.case_data["ENV_DATA"][source]
        except:
            self.env_data = None
        if self.env_data is None:
            self.host = None
        else:
            self.host = self.env_data["HOST"]
        self.url_path = self.case_data["SOURCE"]["URL_PATH"]
        self.source = self.case_data["SOURCE"][source]
        self.url = self.case_data["SOURCE"][source]["URL"]
        self.headers = self.source["HEADERS"]
        self.headers_type = self.headers["TYPE"]
        self.headers_data = self.headers["DATA"]
        self.params = self.source["PARAMS"]
        self.params_type = self.params["TYPE"]
        self.params_data = self.params["DATA"]
        self.request_mode = self.case_data["SOURCE"]["METHOD"]
        self.request_body = self.source["BODY"]
        self.body_type = self.request_body["TYPE"]
        self.body_data = self.request_body["DATA"]
        self.assert_data_format = self.case_data["ASSERT"]["DATA_FORMAT"]
        self.assert_data_content = self.case_data["ASSERT"]["DATA_CONTENT"][source]
        self.another_assert_data = self.case_data["ASSERT"]["ANOTHER_ASSERT"]
        self.another_assert_fail_list = []
        self.fail_list = []
        self.requests_data = {"headers": self.get_headers(), "url": self.get_url(), "body": self.get_body()}
        self.response = None

    def get_headers(self):
        if self.headers_type == "NORMAL":
            return self.headers_data
        headers_func = header_function_import(self.headers_type)
        return headers_func(func_data=self.headers_data, case_data=self.case_data)

    def get_url(self):
        if self.host is not None:
            self.url = self.host + self.url_path
        if self.params_data is None:
            return self.url
        if self.params_type == "JOIN":
            return self.url + "?" + urlencode(self.params_data)

    def get_body(self):
        if self.request_mode == "GET":
            return None
        if self.request_mode == "POST" and self.body_type == "JSON":
            return json.dumps(self.body_data)
        body_func = body_function_import(self.body_type)
        self.body_type = "JSON"
        return body_func(func_data=self.body_data, case_data=self.case_data)

    def format_assert(self):
        if self.response.status_code == 200:
            response_code_result = True
        else:
            response_code_result = False
            msg = "请求结果非200,Code为:{}".format(str(self.response.status_code))
            self.fail_list.append({"reason": msg, "case": None, "response": self.response.text})
        if self.assert_data_format is not None and response_code_result:
            format_result = self.inspection_method.structure_format_diff(self.assert_data_format, self.response)
            if format_result is False:
                self.inspection_method.fail_list_assert()
                self.inspection_method.fail_list = []
            else:
                self.inspection_method.fail_list = []

    def content_assert(self):
        if self.assert_data_content is not None and self.inspection_method.response_content_check(
                self.assert_data_content, self.response) is False:
            self.inspection_method.fail_list_assert()
            self.inspection_method.fail_list = []
        else:
            self.inspection_method.fail_list = []

    def another_assert(self):
        if self.another_assert_data is None:
            return
        if isinstance(self.another_assert_data, list):
            for assert_data in self.another_assert_data:
                function_name = assert_data["TYPE"]
                function_data = assert_data["DATA"]
                func = assert_function_import(function_name)
                func(func_data=function_data, case_data=self.case_data, response=self.response,
                     fail_list=self.another_assert_fail_list)
        else:
            function_name = self.another_assert_data["TYPE"]
            function_data = self.another_assert_data["DATA"]
            func = assert_function_import(function_name)
            func(func_data=function_data, case_data=self.case_data, response=self.response,
                 fail_list=self.another_assert_fail_list)

    def another_assert_report(self):
        msg = ""
        if len(self.another_assert_fail_list) > 0:
            for i in self.another_assert_fail_list:
                msg = "\n" + msg + i + "\n"
                msg = msg + "\n"
            assert False, msg

    def error_message(self):
        for fail in self.fail_list:
            print("Headers:", fail["request_data"]["headers"])
            print("Url:", fail["request_data"]["url"])
            print("Body:", fail["request_data"]["body"])
            print("Mode:", self.request_mode)
            print("Response:", fail["response"])

    def api_test(self):
        if self.request_mode == "GET":
            response = requests.get(url=self.requests_data["url"], headers=self.requests_data["headers"])
        else:
            if self.body_type == "JSON":
                response = requests.post(url=self.requests_data["url"], headers=self.requests_data["headers"],
                                         json=self.requests_data["body"])
        self.response = response


def single_api_tester(yaml_path, source="online"):
    config = config_reader(yaml_path)
    a = ApiTester(config)
    a.api_test()
    if len(a.fail_list) > 0:
        return False
    else:
        return True


if __name__ == "__main__":
    single_api_tester("./../case/all/test.yml")
