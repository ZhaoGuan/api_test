#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import os
from basics_function.golable_function import config_reader

PATH = os.path.dirname(os.path.abspath(__file__))


def env_data(case_path, path):
    config = config_reader(path)
    path_name_list = config.keys()
    for path_name in path_name_list:
        if path_name in case_path:
            return config[path_name]
    return None


class TestCaseMaker:
    def __init__(self, path, source="online", config_path=PATH + "/../env_config/config"):
        self.case_data = config_reader(path)
        self.env_config = env_data(path, config_path)
        self.case_data["ENV_DATA"] = self.env_config
        self.url = self.case_data["SOURCE"]["URL_PATH"]
        try:
            self.DATA_TYPE = self.source["SOURCE"]["DATA_TYPE"]
        except:
            self.DATA_TYPE = "ONLY"
        self.source = self.case_data["SOURCE"][source]
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

    def case_result(self):
        if self.DATA_TYPE == "ONLY":
            return self.case_data
