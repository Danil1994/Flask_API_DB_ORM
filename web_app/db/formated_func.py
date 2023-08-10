"""func which handle and serialize response to json or xml format."""
from __future__ import annotations

import functools
import json
import xml.etree.ElementTree as ET

from dict2xml import dict2xml
from flask import Response, request

from web_app.constants import MyEnum


def serialize_model(model) -> {str: str}:
    return {
        'object': str(model)
    }


# convert dict to json/xml
def output_formatted_data_from_dict(format_value: MyEnum, info_list: list[any] | dict) -> Response:
    if format_value == MyEnum.XML:
        resp = dict2xml(info_list, indent=" ")
        return Response(response=resp, status=200, headers={'Content-Type': 'application/xml'})
    else:
        json_str = json.dumps(info_list)
        return Response(response=json_str.encode('utf-8'), status=200, headers={'Content-Type': 'application/json'})


# convert list to json/xml
def output_formatted_data_from_list(format_value: MyEnum, info_list: list[any] | dict,
                                    element_name: str = 'element') -> Response:
    if format_value == MyEnum.XML:
        elements = ET.Element("response")

        for item_info in info_list:
            element = ET.SubElement(elements, element_name)
            if isinstance(item_info, dict):
                for key, value in item_info.items():
                    ET.SubElement(element, key).text = str(value)
            else:
                ET.SubElement(element, "value").text = str(item_info)

        resp = ET.tostring(elements, encoding="unicode")

        return Response(response=resp, status=200, headers={'Content-Type': 'application/xml'})
    else:
        json_list = [serialize_model(model) for model in info_list]
        json_str = json.dumps(json_list)
        return Response(response=json_str.encode('utf-8'), status=200, headers={'Content-Type': 'application/json'})


# decorator which convert fucn result to json/xml format depending on the response format and type of fucn result
def output_formatted_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_result = func(*args, **kwargs)
        response_format = MyEnum(request.args.get('format', default='json'))
        if type(func_result) is list:
            return output_formatted_data_from_list(response_format, func_result)
        else:
            return output_formatted_data_from_dict(response_format, func_result)

    return wrapper
