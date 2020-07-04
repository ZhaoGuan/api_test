#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from basics_function.golable_function import config_reader


class TestCaseMaker:
    def __init__(self, path, source):
        self.case_data = config_reader(path)
        self.source = self.case_data["SOURCE"][source]
        self.url = self.source["URL"]
        try:
            self.DATA_TYPE = self.source["DATA_TYPE"]
        except:
            self.DATA_TYPE = "ONLY"
        self.headers = self.source["HEADERS"]
        self.headers_type = self.headers["TYPE"]
        self.headers_data = self.headers["DATA"]
        self.params = self.source["PARAMS"]
        self.params_type = self.params["TYPE"]
        self.params_data = self.params["DATA"]
        self.request_mode = self.source["MODE"]["TYPE"]
        self.request_body = self.source["BODY"]
        self.body_type = self.request_body["TYPE"]
        self.body_data = self.request_body["DATA"]
        self.assert_data_format = self.case_data["DATA_FORMAT"]
        self.assert_data_content = self.case_data["DATA_CONTENT"]

    def case_result(self):
        if self.DATA_TYPE == "ONLY":
            return self.case_data
