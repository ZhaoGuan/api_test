#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from basics_function.golable_function import MD5, config_reader

import time
import copy
import requests
import json
import threading
import os
import uuid

PATH = os.path.dirname(os.path.abspath(__file__))


class FiveNut:
    def __init__(self, fail_list):
        self.salt = config_reader(PATH + "/../config/salt.yml")["salt"]
        self.fail_list = fail_list
        self.time_stamp = int(round(time.time() * 1000))
        self._value_lock = threading.Lock()
        self.duid = None

    def wuren_date_duid(self):
        duid = "gz_random_" + str(uuid.uuid1())
        return duid

    def get_sign_old(self, data):
        header_data = data["headers"]
        try:
            duid = header_data["duid"]
        except:
            assert False, "header 中没有duid"
        try:
            language = header_data["lang"]
        except:
            assert False, "header 中没有lang"
        try:
            version = header_data["version"]
        except:
            assert False, "header 中没有version"
        data = duid + "_" + language + "_" + str(self.time_stamp) + "_" + str(version) + "_" + self.salt
        result = MD5(data)
        return result

    def get_sign(self, data):
        header_data = data["headers"]
        try:
            duid = header_data["duid"]
        except:
            assert False, "header 中没有duid"
        try:
            language = header_data["lang"]
        except:
            assert False, "header 中没有lang"
        try:
            version = header_data["version"]
        except:
            assert False, "header 中没有version"
        try:
            app_code = header_data["app_code"]
        except:
            assert False, "header 中没有app_code"
        data = duid + "_" + language + "_" + str(self.time_stamp) + "_" + str(version) + "_" + str(
            app_code) + "_" + self.salt
        result = MD5(data)
        return result

    def set_header(self, data):
        header_data = data["headers"]
        try:
            duid = header_data["duid"]
        except:
            assert False, "header 中没有duid"
        try:
            language = header_data["lang"]
        except:
            assert False, "header 中没有lang"
        try:
            version = header_data["version"]
        except:
            assert False, "header 中没有version"
        try:
            app_code = header_data["app_code"]
        except:
            assert False, "header 中没有app_code"
        if duid == "RANDOM":
            duid = self.wuren_date_duid()
            # 替换duid数据
            data["headers"]["duid"] = duid
        new_header_data = copy.deepcopy(header_data)
        new_header_data.pop("duid")
        new_header_data.pop("lang")
        new_header_data.pop("version")
        new_header_data.pop("app_code")
        new_header_data.update(
            {"User-Agent": duid + "#&#" + language + "#&#" + str(self.time_stamp) + "#&#" + str(version)
                           + "#&#" + str(app_code), 'Content-Type': 'application/json;charset=UTF-8', })
        return new_header_data

    def get_token(self, data, headers, source):
        print(data)
        print(headers)
        app_code = headers["User-Agent"].split("#&#")[-1]
        sign = self.get_sign(data)
        if source == "test":
            token_url = "http://api.dev.5nuthost.com:8080/v1/identity/account/login/device"
        else:
            token_url = "https://api.5nuthost.com/v1/identity/account/login/device"
        try:
            response = requests.post(token_url, json={"sign": sign, "appCode": app_code}, headers=headers)
            print(response.text)
            token = json.loads(response.text)["info"]["token"]
            print(token)
        except Exception as e:
            print(e)
            assert False, "获取token错误"
        return token

    def get_esa_token(self, data, headers, source):
        print(data)
        print(headers)
        app_code = headers["User-Agent"].split("#&#")[-1]
        sign = self.get_sign(data)
        if source == "test":
            token_url = "http://api.dev.5nuthost.com:8080/v1/identity/account/login/device"
        else:
            token_url = "https://api.5nuthost.com/v1/identity/account/login/device"
        try:
            response = requests.post(token_url, json={"sign": sign, "appCode": app_code}, headers=headers)
            print(response.text)
            token = json.loads(response.text)["info"]["token"]
            print(token)
        except:
            print(response.text)
            assert False, "获取token错误"
        return token
