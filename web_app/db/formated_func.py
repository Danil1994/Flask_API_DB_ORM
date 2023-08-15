"""func which handle and serialize response to json or xml format."""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET

from dict2xml import dict2xml
from flask import Response

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
