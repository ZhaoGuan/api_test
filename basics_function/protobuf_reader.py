#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from protobuf import commonResponse_pb2
from protobuf import wallPapper_pb2
from google.protobuf.json_format import MessageToJson
import json


def common(response):
    cr = commonResponse_pb2.CommonResponse()
    cr.ParseFromString(response.content)
    data = MessageToJson(cr)
    result = json.loads(data)
    result["info"].pop("@type")
    return json.dumps(result)
