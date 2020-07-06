#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'

def example(func_data, fail_list, case_data=None):
    print(func_data)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    msg = "编辑下要输出的错误信息到这里，具体内容请自己设计"
    print(msg)
    print(case_data)
    fail_list.append(msg)
