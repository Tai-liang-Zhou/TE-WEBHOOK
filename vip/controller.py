# -*- coding: utf-8 -*-
from flask import Response
from flask import request
from flask_restful import Resource
import json

def setup_route(api):
    """
        return map of endpoint and handler
    """
    api.add_resource(UrgeRefundListAllOrderHandler, '/urge_refund/list_all_order')
    api.add_resource(UrgeRefundGetOrderInfoHandler, '/urge_refund/get_order_info')
    api.add_resource(UrgeLogisticsListAllOrderHandler, '/urge_logistics/list_all_order')
    api.add_resource(UrgeLogisticsGetOrderInfoHandler, '/urge_logistics/get_order_info')
    api.add_resource(HealthCheckHandler, '/_health_check')

def encapsule_rtn_format(kv_map):
    return {
                "status_code": 0,
                "msg_response": {
                    "update": kv_map
                }
            }

class UrgeLogisticsListAllOrderHandler(Resource):
    def post(self):
        json_from_request = json.loads(request.stream.read())
        user_id = json_from_request['task_info']['vip_user_id']
        kv_map = None
        if user_id == '001':
            kv_map = {
                "second_ask": "false",
                "order_length": 4,
                "order":{
                    "type": "order_list",
                    "order_list": [
                        {
                        "order_id": "16100567243327",
                        "item_list": [
                            {
                            "item": "棕色高帮英伦复古商务皮靴",
                            "description": "清仓-侧恩ceen男鞋专场尺码40",
                            "price": "338"
                            }
                        ],
                        "total_price": "338"
                        },
                        {
                        "order_id": "16100567243328",
                        "item_list": [
                            {
                            "item": "棕色高帮英伦复古商务皮靴",
                            "description": "清仓-侧恩ceen男鞋专场尺码40",
                            "price": "338"
                            }
                        ],
                        "total_price": "338"
                        },
                        {
                        "order_id": "16100567243329",
                        "item_list": [
                            {
                            "item": "棕色高帮英伦复古商务皮靴",
                            "description": "清仓-侧恩ceen男鞋专场尺码40",
                            "price": "338"
                            }
                        ],
                        "total_price": "338"
                        },
                        {
                        "order_id": "16100567243330",
                        "item_list": [
                            {
                            "item": "棕色高帮英伦复古商务皮靴",
                            "description": "清仓-侧恩ceen男鞋专场尺码40",
                            "price": "338"
                            }
                        ],
                        "total_price": "338"
                        }
                    ]
                }
            }
        elif user_id == '002':
            kv_map = {
                "second_ask": "false",
                "order_length": 1,
                "order":{
                    "type": "order_list",
                    "order_list": [
                        {
                        "order_id": "16100567243331",
                        "item_list": [
                            {
                            "item": "棕色高帮英伦复古商务皮靴",
                            "description": "清仓-侧恩ceen男鞋专场尺码40",
                            "price": "338"
                            }
                        ],
                        "total_price": "338"
                        }
                    ]
                }
            }
        elif user_id == '003':
            kv_map = {
                "second_ask": "true",
                "deadline": "2017-06-29"
            }
        else:
            pass
        ret = encapsule_rtn_format(kv_map)
        return Response(json.dumps(ret), status=200)

class UrgeLogisticsGetOrderInfoHandler(Resource):
    def post(self):
        json_from_request = json.loads(request.stream.read())
        order_id = json_from_request['task_info']['order_id']
        kv_map = None
        if order_id == '16100567243327':
            kv_map = {
                "can_be_urged": "true",
                "deliver": "true",
                "timeout": "false",
                "deadline": "2017-06-15"
            }
        elif order_id == '16100567243328':
            kv_map = {
                "can_be_urged": "true",
                "deliver": "true",
                "timeout": "true",
                "deadline": "2017-06-15"
            }
        elif order_id == '16100567243329':
            kv_map = {
                "can_be_urged": "true",
                "deliver": "false",
                "timeout": "true"
            }
        elif order_id == '16100567243330':
            kv_map = {
                "can_be_urged": "true",
                "deliver": "false",
                "timeout": "false"
            }
        elif order_id == '16100567243331':
            kv_map = {
                "can_be_urged": "false"
            }
        else:
            pass
        ret = encapsule_rtn_format(kv_map)
        return Response(json.dumps(ret), status=200)

class UrgeRefundListAllOrderHandler(Resource):
    def post(self):
        json_from_request = json.loads(request.stream.read())
        user_id = json_from_request['task_info']['vip_user_id']
        kv_map = None
        if user_id == '001':
            kv_map = {
                "second_ask": "false",
                "order_length": 4,
                "order":{
                    "type": "order_list",
                    "order_list": [
                        {
                        "order_id": "16100567243327",
                        "item_list": [
                            {
                            "item": "棕色高帮英伦复古商务皮靴",
                            "description": "清仓-侧恩ceen男鞋专场尺码40",
                            "price": "338"
                            }
                        ],
                        "total_price": "338"
                        },
                        {
                        "order_id": "16100567243328",
                        "item_list": [
                            {
                            "item": "棕色高帮英伦复古商务皮靴",
                            "description": "清仓-侧恩ceen男鞋专场尺码40",
                            "price": "338"
                            }
                        ],
                        "total_price": "338"
                        },
                        {
                        "order_id": "16100567243329",
                        "item_list": [
                            {
                            "item": "棕色高帮英伦复古商务皮靴",
                            "description": "清仓-侧恩ceen男鞋专场尺码40",
                            "price": "338"
                            }
                        ],
                        "total_price": "338"
                        },
                        {
                        "order_id": "16100567243330",
                        "item_list": [
                            {
                            "item": "棕色高帮英伦复古商务皮靴",
                            "description": "清仓-侧恩ceen男鞋专场尺码40",
                            "price": "338"
                            }
                        ],
                        "total_price": "338"
                        }
                    ]
                }
            }
        elif user_id == '002':
            kv_map = {
                "second_ask": "false",
                "order_length": 1,
                "order":{
                    "type": "order_list",
                    "order_list": [
                        {
                        "order_id": "16100567243327",
                        "item_list": [
                            {
                            "item": "棕色高帮英伦复古商务皮靴",
                            "description": "清仓-侧恩ceen男鞋专场尺码40",
                            "price": "338"
                            }
                        ],
                        "total_price": "338"
                        }
                    ]
                }
            }
        elif user_id == '003':
            kv_map = {
                "second_ask": "true",
                "deadline": "2017-06-29"
            }
        else:
            pass
        ret = encapsule_rtn_format(kv_map)
        return Response(json.dumps(ret), status=200)

class UrgeRefundGetOrderInfoHandler(Resource):
    def post(self):
        json_from_request = json.loads(request.stream.read())
        order_id = json_from_request['task_info']['order_id']
        kv_map = None
        if order_id == '16100567243327':
            kv_map = {
                "already_apply_refund": "true",
                "deadline": "2017-06-29"
            }
        elif order_id == '16100567243328':
            kv_map = {
                "already_apply_refund": "false",
                "already_return_cargo": "true"
            }
        elif order_id == '16100567243329':
            kv_map = {
                "already_apply_refund": "false",
                "already_return_cargo": "false",
                "already_apply_return_cargo": "true",
                "fast_refund": "false"
            }
        elif order_id == '16100567243330':
            kv_map = {
                "already_apply_refund": "false",
                "already_return_cargo": "false",
                "already_apply_return_cargo": "false",
                "fast_refund": "true"
            }
        else:
            pass
        ret = encapsule_rtn_format(kv_map)
        return Response(json.dumps(ret), status=200)

class HealthCheckHandler(Resource):
    def get(self):
        resp = Response()
        resp.data = u'ok'
        return resp