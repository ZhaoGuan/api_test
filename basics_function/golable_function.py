#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import yaml
import sys, getopt
import hashlib
from urllib import parse
from PIL import Image
import requests
import io


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


if __name__ == "__main__":
    import requests

    response = requests.get("https://static.cdn.5nuthost.com/package/bf6ee9406aad7bcd572d119dc0e61128.apk")
    a = get_response_content_md5(response.content)
    print(a)
