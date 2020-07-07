#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import os
from basics_function.golable_function import config_reader
import copy

PATH = os.path.dirname(os.path.abspath(__file__))


def env_data(case_path, path):
    config = config_reader(path)
    path_name_list = config.keys()
    for path_name in path_name_list:
        if path_name in case_path:
            return config[path_name]
    return None


def key_value_twice_replace(base_data, replace_data):
    for k, v in replace_data.items():
        if v is None:
            base_data[k] = v
        else:
            for v_k, v_v in v.items():
                base_data[k][v_k] = v_v


class TestCaseMaker:
    def __init__(self, path, source="online", config_path=PATH + "/../env_config/config"):
        self.source_name = source
        self.case_data = config_reader(path)
        self.env_config = env_data(path, config_path)
        self.case_data["ENV_DATA"] = self.env_config
        self.url = self.case_data["SOURCE"]["URL_PATH"]
        try:
            self.DATA_TYPE = self.case_data["SOURCE"]["DATA_TYPE"]
        except:
            self.DATA_TYPE = "ONLY"
        self.source = self.case_data["SOURCE"][self.source_name]
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
        try:
            self.assert_data_format = self.case_data["ASSERT"]["DATA_FORMAT"]
            try:
                self.assert_data_format_data = self.case_data["ASSERT"]["DATA_FORMAT"]["DATA"]
            except:
                self.case_data["ASSERT"]["DATA_FORMAT"]["DATA"] = None
        except:
            self.case_data["ASSERT"]["DATA_FORMAT"] = None
        try:
            self.assert_data_content = self.case_data["ASSERT"]["DATA_CONTENT"]
            try:
                self.assert_data_content_source = self.case_data["ASSERT"]["DATA_CONTENT"][self.source_name]
            except:
                self.case_data["ASSERT"]["DATA_CONTENT"] = {self.source_name: None}
        except:
            self.case_data["ASSERT"]["DATA_CONTENT"] = None
        try:
            self.another_assert_another_assert = self.case_data["ASSERT"]["ANOTHER_ASSERT"]
            try:
                self.another_assert_another_assert_source = self.case_data["ASSERT"]["ANOTHER_ASSERT"][self.source_name]
            except:
                self.case_data["ASSERT"]["ANOTHER_ASSERT"] = {self.source_name: None}
        except:
            self.case_data["ASSERT"]["ANOTHER_ASSERT"] = None

    def replace_case_data(self, new_data):
        if new_data["PATH"] is None:
            return
        replace_data = new_data["SOURCE"][self.source_name]
        replace_assert = new_data["ASSERT"]
        result = new_data["ABOVE"]
        key_value_twice_replace(self.case_data["SOURCE"][self.source_name], replace_data)
        key_value_twice_replace(self.case_data["ASSERT"], replace_assert)
        self.case_data["ABOVE"] = result

    def more_cases_data_header(self, keys, more_data):
        if isinstance(self.headers_data, list):
            for i in self.headers_data:
                key = list(i.keys())[0]
                value = list(i.values())[0]
                keys.append(key)
                more_data["headers"][key] = value
        else:
            more_data["headers"] = None

    def more_cases_data_params(self, keys, more_data):
        if isinstance(self.params_data, list):
            for i in self.params_data:
                key = list(i.keys())[0]
                value = list(i.values())[0]
                keys.append(key)
                more_data["params"][key] = value
        else:
            more_data["params"] = None

    def more_cases_data_body(self, keys, more_data):
        if isinstance(self.body_data, list):
            for i in self.body_data:
                key = list(i.keys())[0]
                value = list(i.values())[0]
                keys.append(key)
                more_data["body"][key] = value
        else:
            more_data["body"] = None

    def more_cases_data_data_content(self, keys, more_data):
        if self.case_data["ASSERT"]["DATA_CONTENT"] is not None and isinstance(
                self.case_data["ASSERT"]["DATA_CONTENT"][self.source_name], list):
            for i in self.case_data["ASSERT"]["DATA_CONTENT"][self.source_name]:
                key = list(i.keys())[0]
                value = list(i.values())[0]
                keys.append(key)
                more_data["data_content"][key] = value
        else:
            more_data["data_content"] = None

    def more_cases_data_another_assert(self, keys, more_data):
        if self.case_data["ASSERT"]["ANOTHER_ASSERT"] is not None and isinstance(
                self.case_data["ASSERT"]["ANOTHER_ASSERT"][self.source_name], list):
            for i in self.case_data["ASSERT"]["ANOTHER_ASSERT"][self.source_name]:
                key = list(i.keys())[0]
                value = list(i.values())[0]
                keys.append(key)
                more_data["another_assert"][key] = value
        else:
            more_data["another_assert"] = None

    def more_cases_data(self):
        keys = []
        more_data = {"headers": {}, "params": {}, "body": {}, "data_content": {}, "another_assert": {}}
        self.more_cases_data_header(keys, more_data)
        self.more_cases_data_params(keys, more_data)
        self.more_cases_data_body(keys, more_data)
        self.more_cases_data_data_content(keys, more_data)
        self.more_cases_data_another_assert(keys, more_data)
        keys = list(set(keys))
        return keys, more_data

    def more_cases(self):
        keys, more_data = self.more_cases_data()
        more_case_result = []
        for key in keys:
            temp_case_data = copy.deepcopy(self.case_data)
            if more_data["headers"] is not None:
                temp_case_data["SOURCE"][self.source_name]["HEADERS"]["DATA"] = more_data["headers"][key]
            if more_data["params"] is not None:
                temp_case_data["SOURCE"][self.source_name]["PARAMS"]["DATA"] = more_data["params"][key]
            if more_data["body"] is not None:
                temp_case_data["SOURCE"][self.source_name]["BODY"]["DATA"] = more_data["body"][key]
            if more_data["data_content"] is not None:
                temp_case_data["ASSERT"]["DATA_CONTENT"][self.source_name] = more_data["data_content"][key]
            if more_data["another_assert"] is not None:
                temp_case_data["ASSERT"]["ANOTHER_ASSERT"][self.source_name] = more_data["another_assert"][key]
            more_case_result.append(temp_case_data)
        return more_case_result

    def case_result(self):
        if self.DATA_TYPE == "ONLY":
            return self.case_data
        else:
            return self.more_cases()
