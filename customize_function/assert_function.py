#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'

def example(func_data, fail_list, response, case_data=None, source_name=None):
    print(func_data)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    msg = "编辑下要输出的错误信息到这里，具体内容请自己设计"
    print(msg)
    print(case_data)
    print(response.text)
    fail_list.append(msg)
