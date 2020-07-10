#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import pytest


def pytest_addoption(parser):
    parser.addoption("--result_print", action="store",
                     default="false",
                     help="将命令行参数 ’--cmdopt' 添加到 pytest 配置中")


@pytest.fixture
def cmdopt(request):
    return request.config.getoption("--result_print")
