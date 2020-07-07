#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import yaml
import sys, getopt
import hashlib
from urllib import parse
from PIL import Image
import requests
import os
import importlib
import random
import time


def url_parse(url):
    scheme, netloc, path, params, query, fragment = parse.urlparse(url)
    if scheme is "" or netloc is "" or path in "":
        return False
    else:
        return {"host": netloc, "path": path, "scheme": scheme}


def config_reader(yaml_file):
    yf = open(yaml_file)
    yx = yaml.safe_load(yf)
    yf.close()
    return yx


def config_data_path(yaml_file):
    yf = open(yaml_file)
    yx = yaml.safe_load(yf)
    yf.close()
    return {"data": yx, "path": yaml_file}


def source_input():
    argv = sys.argv[1:]
    source = None
    try:
        opts, args = getopt.getopt(argv, "h:s:", ["source="])
    except getopt.GetoptError:
        print('xxx.py  -s <source>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('xx.py -s <source>')
            sys.exit()
        elif opt in ("-s", "--source"):
            source = arg
        else:
            print('失败,未填写source')
    return source


def md5(data):
    m = hashlib.md5()
    m.update(data.encode('utf-8'))
    MD5 = m.hexdigest()
    return MD5


def get_response_content_md5(response_content):
    md5_obj = hashlib.md5()
    md5_obj.update(response_content)
    hash_code = md5_obj.hexdigest()
    md5 = str(hash_code).lower()
    return md5


def list_duplicate_removal(data):
    result = []
    for i in data:
        if i not in result:
            result.append(i)
    return result


def get_key_value_list(keys, data):
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
            data = False
    return data


def temp_yml(data, path):
    try:
        os.makedirs(path)
    except:
        pass
    temp_path = path + str(int(time.time())) + ".yml"
    with open(path + str(int(time.time())) + ".yml", "w") as f:
        yaml.dump(data, f)
    return temp_path


def assert_function_import(function_name):
    assert_function = importlib.import_module("customize_function.assert_function", ".")
    run = getattr(assert_function, function_name)
    return run


def header_function_import(function_name):
    header_function = importlib.import_module("customize_function.header_function", ".")
    run = getattr(header_function, function_name)
    return run


def body_function_import(function_name):
    body_function = importlib.import_module("customize_function.body_function", ".")
    run = getattr(body_function, function_name)
    return run


def above_function_import(function_name):
    above_function = importlib.import_module("customize_function.above_function", ".")
    run = getattr(above_function, function_name)
    return run
