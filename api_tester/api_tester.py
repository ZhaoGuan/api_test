#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from basics_function.golable_function import config_reader
from basics_function.Inspection_method import InspectionMethod
from urllib.parse import urlencode
import json
import requests


class ApiTester:
    def __init__(self, config, source="online"):
        self.inspection_method = InspectionMethod()
        self.case_data = config
        try:
            self.env_data = self.case_data["ENV_DATA"]
        except:
            self.env_data = None
        if self.env_data is None:
            self.host = None
        else:
            self.host = self.case_data["HOST"]
        self.url_path = self.case_data["SOURCE"]["URL_PATH"]
        self.source = self.case_data["SOURCE"][source]
        self.url = self.case_data["SOURCE"][source]["URL"]
        self.headers = self.source["HEADERS"]
        self.headers_type = self.headers["TYPE"]
        self.headers_data = self.headers["DATA"]
        self.params = self.source["PARAMS"]
        self.params_type = self.params["TYPE"]
        self.params_data = self.params["DATA"]
        self.request_mode = self.source["METHOD"]
        self.request_body = self.source["BODY"]
        self.body_type = self.request_body["TYPE"]
        self.body_data = self.request_body["DATA"]
        self.assert_data_format = self.case_data["ASSERT"]["DATA_FORMAT"]
        self.assert_data_content = self.case_data["ASSERT"]["DATA_CONTENT"]["online"]
        self.fail_list = []
        self.requests_data = {"headers": self.get_headers(), "url": self.get_url(), "body": self.get_body()}
        self.response = None

    def get_headers(self):
        if self.headers_type == "NORMAL":
            return self.headers_data

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

    def api_assert(self):
        if self.response.status_code == 200:
            response_code_result = True
        else:
            response_code_result = False
            self.fail_list.append({"request_data": self.requests_data, "response": self.response.text})
        try:
            response_json = json.loads(self.response.text)
        except Exception as e:
            print("Json 解析错误", e)
            response_json = False
            self.fail_list.append({"request_data": self.requests_data, "response": self.response.text})
        if self.assert_data_format is not None and response_code_result and response_json:
            format_result = self.inspection_method.structure_format_diff(self.assert_data_format, response_json)
            if format_result is False:
                self.inspection_method.fail_list_assert()
            else:
                self.inspection_method.fail_list = []

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
        # self.api_assert(response, requests_data)


def single_api_tester(yaml_path, source="online"):
    config = config_reader(yaml_path)
    a = ApiTester(config)
    a.api_test()
    if len(a.fail_list) > 0:
        return False
    else:
        return True


if __name__ == "__main__":
    single_api_tester("./../case/all/verity_roomtype.yml")
