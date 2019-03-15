# -*- coding: utf-8 -*-
from flask import Response
from flask import request
from flask_restful import Resource
from dateutil.parser import parse
from langconv import Converter
from datetime import datetime
import json
import re
import requests
import constants
import logging
LOG = logging.getLogger(__name__)


def setup_route(api):
    """
        return map of endpoint and handler
    """
    api.add_resource(ConvertParams, '/restaurant/convert_params')
    api.add_resource(ConvertParamsNLU1, '/restaurant/convert_params_nlu1')
    api.add_resource(ConvertParamsNLU2, '/restaurant/convert_params_nlu2')
    
    api.add_resource(SearchRestaurant, '/restaurant/search')
    api.add_resource(BookRestaurant, '/restaurant/book')
    api.add_resource(ListMoreOptions, '/restaurant/more_opts')
    api.add_resource(ListRequerements, '/restaurant/requirements')
    api.add_resource(UpdateRequerements, '/restaurant/opd_requirements')
    api.add_resource(ResetParams, '/restaurant/reset_params')

    api.add_resource(SearchReserveOrderByPhone, '/reserve_order/search_by_phone')
    api.add_resource(SearchReserveOrderBySeriesNumber, '/reserve_order/search_by_series_number')
    api.add_resource(CancelReserveOrder, '/reserve_order/cancel')
    api.add_resource(EditReserveOrder, '/reserve_order/edit')

    # inline booking
    api.add_resource(InlineStartBooking, '/VBooking/rest/inline/startBooking')
    api.add_resource(InlineDoBooking, '/VBooking/rest/inline/doBooking')
    api.add_resource(InlineEndBooking, '/VBooking/rest/inline/endBooking')

def encapsule_rtn_format(update_kv_map, remove_kv_map):
    rtn_obj = {
                "status_code": 0,
                "msg_response": {}
            }
    if update_kv_map is not None:
        rtn_obj['msg_response']['update'] = update_kv_map
    if remove_kv_map is not None:
        rtn_obj['msg_response']['remove'] = remove_kv_map
    return rtn_obj

def get_num(num_str):
    # turn the number represented by chinese to number string.
    payload = {
        "id": "integer-number",
        "hasContext": False,
        "query": Converter('zh-hans').convert(num_str)
    }
    payload = json.dumps(payload, ensure_ascii=False)
    payload = payload.encode('utf-8')
    headers = {'content-type': 'application/json'}
    r = requests.post(constants.TDE_URL, payload, timeout=float(constants.REQUEST_TIMEOUT), headers=headers)
    r_obj = r.json()
    # LOG.info(json.dumps(r_obj, ensure_ascii=False, indent=4))
    try :
        num = r_obj['informs'][0]['value']['displayText']
    except :
        num = None
        LOG.error('type error form num_str')
    return num

def get_phone_num(num_str):
    # turn the phone number represented by chinese to number string.
    payload = {
        "id": "phone",
        "hasContext": False,
        "arguments":{
                "regions" : ["mainland","tw"],
                "types":["mobile","landline"]
               },
        "query": Converter('zh-hans').convert(num_str)
    }
    payload = json.dumps(payload, ensure_ascii=False)
    payload = payload.encode('utf-8')
    headers = {'content-type': 'application/json'}
    r = requests.post(constants.TDE_URL, payload, timeout=float(constants.REQUEST_TIMEOUT), headers=headers)
    r_obj = r.json()
    # LOG.info(json.dumps(r_obj, ensure_ascii=False, indent=4))
    try:
        phone = r_obj['informs'][0]['value']['displayText']
    except:
        phone = None
        LOG.error('type error form phone num_str')
    return phone

def get_hourtime(hour_str):
    # get the turely data time ex :  hh:mm:ss 
    payload = {
    "id": "chrono",
    "hasContext": True,
    "arguments": {
        "orientation": "future",
        "timePoint": {
            "onlyOne": "last",
            "distinguishType": False
        },
        "duration": {
            "extract": False,
            "onlyOne": "last"
        }
    },
    "query": Converter('zh-hans').convert(hour_str),
    }
    payload = json.dumps(payload, ensure_ascii=False)
    payload = payload.encode('utf-8')
    headers = {'content-type': 'application/json'}
    r = requests.post(constants.TDE_URL, payload, timeout=float(constants.REQUEST_TIMEOUT), headers=headers)
    # error_msg = 'API invocation fail,url:%s, status_code:%s, response:%s'\
    #             % (constants.TDE_URL, r.status_code, r.text)
    # LOG.error(error_msg)
    r_obj = r.json()

    
    # LOG.info(json.dumps(r_obj, ensure_ascii=False, indent=4))
    minute = 'minute_enable'
    if 'minute' not in r_obj['informs'][0]['value']['chrono']['time']['items'][0]:
        minute = 'minute_disable'
    try:
        hour = r_obj['informs'][0]['value']['chrono']['time']['items'][0]['hour']
    except:
        hour = None
        LOG.error('type error form exact_hour')
    return hour, minute
    
def get_datetime(datetime_str):
    # get the turely data time ex : yyyy-mm-dd hh:mm:ss 
    payload = {
        "id": "chrono",
        "hasContext": True,
        "arguments": {
            "orientation": "future",
            "timePoint": {
                "onlyOne": "last",
                "distinguishType": False
            },
            "duration": {
                "extract": False,
                "onlyOne": "last"
            }
        },
        "query": Converter('zh-hans').convert(datetime_str),
    }
    payload = json.dumps(payload, ensure_ascii=False)
    payload = payload.encode('utf-8')
    headers = {'content-type': 'application/json'}
    r = requests.post(constants.TDE_URL, payload, timeout=float(constants.REQUEST_TIMEOUT), headers=headers)
    # error_msg = 'API invocation fail,url:%s, status_code:%s, response:%s'\
    #             % (constants.TDE_URL, r.status_code, r.text)
    # LOG.error(error_msg)
    r_obj = r.json()
    # LOG.info(json.dumps(r_obj, ensure_ascii=False, indent=4))
    try:
        dt = parse(r_obj['informs'][0]['value']['chrono']['time']['items'][0]['ISO_DATE']['single'])
    except :
        dt = "0001-01-01"
        dt = datetime.strptime(dt, '%Y-%m-%d')
        LOG.error('type error form exact_date')
    return dt



class InlineStartBooking(Resource):
    def post(self):
        json_from_request = json.loads(Converter('zh-hant').convert(request.stream.read().decode('utf-8')))
        user_id = json_from_request['user_id']
        text = json_from_request['text']
        task_info = json_from_request['task_info']
        from_sip = task_info.get('from_sip', '')
        caller_id = task_info.get('caller_id', '')
        payload = {
            "user_id": user_id,
            "text": text,
            "task_info": {
                "from_sip": from_sip,
                "caller_id": caller_id,
            }
        }
        url = constants.SYSTEX_URL+'inline/startBooking'
        LOG.debug('request inline start booking API: %s' % url)
        LOG.debug('payload: %s' % json.dumps(payload, ensure_ascii=False, indent=4))
        r = requests.post(
            url,
            json=payload,
            timeout=float(constants.REQUEST_TIMEOUT)
        )
        r_obj = r.json()
        LOG.debug('response: %s' % json.dumps(r_obj, ensure_ascii=False, indent=4))
        ret = encapsule_rtn_format(r_obj["msg_response"]["update"], None)
        return Response(json.dumps(ret), status=200)


class InlineDoBooking(Resource):
    def post(self):
        json_from_request = json.loads(Converter('zh-hans').convert(request.stream.read().decode('utf-8')))
        task_info = json_from_request['task_info']
        te_payload = {
            "user_id": json_from_request['user_id'],
            "text": json_from_request['text'],
            "task_info": {
                "time_date": task_info.get('time_date', None),
                "time_time": task_info.get('time_time', None),
                "restaurant_id": task_info.get('restaurant_id', None),
                "seat_num": task_info.get('seat_num', None),
                "kid_num": task_info.get('seat_num_children', None),
                "chair_num": task_info.get('chair_num', None) ,# if "chair_num" in task_info else 0
                "lastname": task_info.get('lastname', None),
                "phone": task_info.get('phone', None),
                "note": task_info.get('note', None),
            }
        }
        LOG.debug('In doBooking, data received from TE: %s' % json.dumps(te_payload, ensure_ascii=False, indent=4))

        task_info = te_payload['task_info']
        payload = {
            "user_id": te_payload['user_id'],
            "text": te_payload['text'],
            "task_info": {
                "date": task_info['time_date'] if task_info['time_date'] is not None else '',
                "time": task_info['time_time'] if task_info['time_time'] is not None else '',
                "restaurant_id": task_info['restaurant_id'] if task_info['restaurant_id'] is not None else '',
                "group_num": int(task_info['seat_num']) if task_info['seat_num'] is not None else 0,
                "kid_num": int(task_info['kid_num']) if task_info['kid_num'] is not None and task_info['kid_num'] != "null" else 0,
                "chair_num": int(get_num(task_info['chair_num'])) if task_info['chair_num'] is not None else 0,
                "lastname": task_info['lastname'] if task_info['lastname'] is not None else '',
                "phone": get_phone_num(task_info['phone']) if task_info['phone'] is not None else '',
                "note": task_info['note'] if task_info['note'] is not None else '',
            }
        }
        url = constants.SYSTEX_URL+'inline/doBooking'
        LOG.debug('request inline do booking API: %s' % url)
        LOG.debug('payload: %s' % json.dumps(payload, ensure_ascii=False, indent=4))
        r = requests.post(
            url,
            json=payload,
            timeout=float(constants.REQUEST_TIMEOUT)
        )
        r_obj = r.json()
        LOG.debug('response: %s' % json.dumps(r_obj, ensure_ascii=False, indent=4))
        update_kv_map = r_obj["msg_response"]["update"]
        # Assign 0 to chair_num if user doesn't want any baby chair
        if 'chair_num' not in json_from_request['task_info']:
            update_kv_map['chair_num'] = '0' 
        ret = encapsule_rtn_format(update_kv_map, None)
        return Response(json.dumps(ret), status=200)

class InlineEndBooking(Resource):
    def post(self):
        json_from_request = json.loads(Converter('zh-hant').convert(request.stream.read().decode('utf-8')))
        user_id = json_from_request['user_id']
        text = json_from_request['text']
        task_info = json_from_request['task_info']
        from_sip = task_info.get('from_sip', '')
        caller_id = task_info.get('caller_id', '')
        payload = {
            "user_id": user_id,
            "text": text,
            "task_info": {
                "from_sip": from_sip,
                "caller_id": caller_id,
                "end_status": task_info['end_status']
            }
        }
        url = constants.SYSTEX_URL+'inline/endBooking'
        LOG.debug('request inline end booking API: %s' % url)
        LOG.debug('payload: %s' % json.dumps(payload, ensure_ascii=False, indent=4))
        r = requests.post(
            url,
            json=payload,
            timeout=float(constants.REQUEST_TIMEOUT)
        )
        r_obj = r.json()
        LOG.debug('response: %s' % json.dumps(r_obj, ensure_ascii=False, indent=4))
        
        # ret = encapsule_rtn_format(r_obj["msg_response"], None)
        # return Response(json.dumps(ret), status=200)

class ListRequerements(Resource):
    def post(self):
        json_from_request = json.loads(Converter('zh-hant').convert(request.stream.read().decode('utf-8')))
        user_id = json_from_request['user_id']
        text = json_from_request['text']
        restaurant_id = json_from_request['task_info']['restaurant_id']
        
        # request systex
        payload = {
            "user_id": user_id,
            "text": text,
            "task_info": {                
                "restaurant_id": restaurant_id
            }
        }
        r = requests.post(constants.SYSTEX_URL+'restaurant/qryRestaurantOpts', json=payload, timeout=float(constants.REQUEST_TIMEOUT))
        r_obj = r.json()
        LOG.info(json.dumps(r_obj, ensure_ascii=False))
        
        ret = encapsule_rtn_format(r_obj["msg_response"]["update"], None)
        return Response(json.dumps(ret), status=200)

class UpdateRequerements(Resource):
    def post(self):
        json_from_request = json.loads(Converter('zh-hant').convert(request.stream.read().decode('utf-8')))
        user_id = json_from_request['user_id']
        text = json_from_request['text']
        booking_id = json_from_request['task_info']['booking_id']

        # request systex
        payload = {
            "user_id": user_id,
            "text": text,
            "task_info": {                
                "id": booking_id
            }
        }
        for i in range(1,4):
            if 'opt'+str(i)+'_yn' in json_from_request['task_info']:
                payload['task_info']['opt'+str(i)+'_yn'] = json_from_request['task_info']['opt'+str(i)+'_yn'].replace('yes', 'Y').replace('no', 'N')
            if 'opt'+str(i)+'_num' in json_from_request['task_info']:
                payload['task_info']['opt'+str(i)+'_num'] = json_from_request['task_info']['opt'+str(i)+'_num']
        r = requests.post(constants.SYSTEX_URL+'booking/updBookingOpts', json=payload, timeout=float(constants.REQUEST_TIMEOUT))
        r_obj = r.json()
        LOG.info(json.dumps(r_obj, ensure_ascii=False))
        
        ret = encapsule_rtn_format({}, None)
        return Response(json.dumps(ret), status=200)

class EditReserveOrder(Resource):
    def post(self):
        update_kv_map = {
            "status": "succeed"
        }
        ret = encapsule_rtn_format(update_kv_map, None)
        return Response(json.dumps(ret), status=200)

class CancelReserveOrder(Resource):
    def post(self):
        update_kv_map = {
            "status": "succeed"
        }
        ret = encapsule_rtn_format(update_kv_map, None)
        return Response(json.dumps(ret), status=200)

class ListMoreOptions(Resource):
    def post(self):
        json_from_request = json.loads(request.stream.read())
        if 'more_opts_order' not in json_from_request['task_info']:
            update_kv_map = {
                "more_opts": u"明天晚上六点或是明天晚上八点",
                "more_opts_order": 1
            }
        elif json_from_request['task_info']['more_opts_order'] == 1:
            update_kv_map = {
                "more_opts": u"后天或是大后天",
                "more_opts_order": 2
            }
        elif json_from_request['task_info']['more_opts_order'] == 2:
            update_kv_map = {
                "more_opts": u"南京东路店或是中山店",
                "more_opts_order": 3
            }
        else:
            update_kv_map = {
                "more_opts_order": -1
            }
        ret = encapsule_rtn_format(update_kv_map, None)
        return Response(json.dumps(ret), status=200)

class SearchReserveOrderBySeriesNumber(Resource):
    def post(self):
        json_from_request = json.loads(request.stream.read())
        series_number = json_from_request['task_info']['series_number']
        update_kv_map = None
        if series_number == u'AABB28825252':
            update_kv_map = {
                "restaurant": u"王品牛排",
                "time": "2018-03-19 19:00:00",
                "seat_num": 5
            }
        else:
            pass
        ret = encapsule_rtn_format(update_kv_map, None)
        return Response(json.dumps(ret), status=200)

class SearchReserveOrderByPhone(Resource):
    def post(self):
        json_from_request = json.loads(request.stream.read())
        phone = json_from_request['task_info']['phone']
        update_kv_map = None
        if phone == u'0912345678':
            update_kv_map = {
                "order_list": [
                    {
                        "restaurant": u"王品牛排",
                        "time": "2018-03-19 19:00:00",
                        "seat_num": 5,
                        "series_number": "AABB28825252"
                    }
                ]
            }
        elif phone == u'0912345677':
            update_kv_map = {
                "order_list": [
                    {
                        "restaurant": u"王品牛排",
                        "time": "2018-03-20 19:00:00",
                        "seat_num": 3,
                        "series_number": "AABB28825253"
                    },
                    {
                        "restaurant": u"西堤牛排",
                        "time": "2018-03-28 19:00:00",
                        "seat_num": 4,
                        "series_number": "AABB28825254"
                    }
                ]
            }
        else:
            pass
        ret = encapsule_rtn_format(update_kv_map, None)
        return Response(json.dumps(ret), status=200)

class ConvertParamsNLU1(Resource):
    def post(self):
        json_from_request = json.loads(request.stream.read())
        LOG.info(json.dumps(json_from_request['task_info'], ensure_ascii=False))
        date_time = json_from_request['task_info'][u'用餐时间_utc']
        seat_num_total = json_from_request['task_info'][u'人数_raw']['total']
        restaurant = json_from_request['task_info'][u'餐厅']

        dt = parse(date_time)

        update_kv_map = {
            "restaurant": restaurant,
            "time_date": dt.strftime("%Y%m%d"),
            "time_time": dt.strftime("%H:%M"),
            "time_str": dt.strftime("%Y年%m月%d日%H点%M分"),
            "seat_num_total": seat_num_total
        }
        
        if 'adult' in json_from_request['task_info'][u'人数_raw']:
            update_kv_map['seat_num'] = json_from_request['task_info'][u'人数_raw']['adult']
        if 'child' in json_from_request['task_info'][u'人数_raw']:
            update_kv_map['seat_num_children'] = json_from_request['task_info'][u'人数_raw']['child']

        ret = encapsule_rtn_format(update_kv_map, None)
        return Response(json.dumps(ret), status=200)

class ConvertParamsNLU2(Resource):
    def post(self):
        json_from_request = json.loads(Converter('zh-hans').convert(request.stream.read().decode('utf-8')))

        # print the format of json
        LOG.debug('In ConvertParamsNLU2, data received from TE: %s' % json.dumps(json_from_request['task_info'], ensure_ascii=False, indent=4))

        # parser time
        exact_date = json_from_request['task_info']['exact_date']
        exact_hour = json_from_request['task_info']['exact_hour']
        exact_minute = json_from_request['task_info']['exact_minute']
        time_time = "{hour}:{minute}".format(hour = exact_hour,minute = exact_minute)

        # parse exact date
        dt = get_datetime(exact_date)
        exact_hour = int(get_num(exact_hour))
        exact_minute = int(get_num(exact_minute))

        LOG.info('hour:'+str(exact_hour)+' minute:'+str(exact_minute))
        dt = dt.replace(hour=exact_hour, minute=exact_minute)
        
        update_kv_map = {"time_time": time_time}
        if exact_minute > 0 :
            update_kv_map['time_str'] = dt.strftime("%m{M}%d{d}%H{h}%M{m}").format(M='月', d='日', h='點', m='分')
        else :
            update_kv_map['time_str'] = dt.strftime("%m{M}%d{d}%H{h}").format(M='月', d='日', h='點')
        
        ret = encapsule_rtn_format(update_kv_map, None)
        return Response(json.dumps(ret), status=200)


class ConvertParams(Resource):
    def post(self):
        json_from_request = json.loads(Converter('zh-hans').convert(request.stream.read().decode('utf-8')))

        # print the format of json
        LOG.debug('In ConvertParams, data received from TE: %s' % json.dumps(json_from_request['task_info'], ensure_ascii=False, indent=4))

        # parse seat number
        seat_num = get_num(json_from_request['task_info']['seat_num'])
        seat_num_total = seat_num
            
        # parse children seat number and chair number
        seat_num_children = 0
        if 'seat_num_children' in json_from_request['task_info'] and json_from_request['task_info']['seat_num_children'] != "null":
            seat_num_children = get_num(json_from_request['task_info']['seat_num_children'])
            seat_num_total = int(seat_num_total) + int(seat_num_children)
        # parser date
        exact_date = json_from_request['task_info']['exact_date']
        exact_hour = json_from_request['task_info']['exact_hour']

        exact_minute = '0'
        
        if 'exact_minute' in json_from_request['task_info']:
            exact_minute = json_from_request['task_info']['exact_minute']
            if exact_minute == u'半':
                exact_minute = '30'

        # parse exact date
        dt = get_datetime(exact_date)

        time_judge = re.compile(u'(早|晚|凌晨|上午|中午|下午|晚上)').search(exact_hour)
        if time_judge is not None:
            time_judge = time_judge.group(1)

        exact_hour, minute = get_hourtime(exact_hour)
        if minute == 'minute_disable':
            exact_minute = '0'

        # opening hours from 9am to 10pm 

        if time_judge in [u'晚',u'中午',u'下午',u'晚上']:
            if exact_hour < 12:
                exact_hour += 12

        if exact_hour < 10:
            exact_hour += 12
        elif exact_hour > 22:
            exact_hour-=12

        exact_minute = int(get_num(str(exact_minute)))

        # LOG.info('hour:'+str(exact_hour)+' minute:'+str(exact_minute))

        dt = dt.replace(hour=exact_hour, minute=exact_minute)

        update_kv_map = {
            "time_date": dt.strftime("%Y%m%d"),
            "time_time": dt.strftime("%H:%M"),
            "exact_minute" : exact_minute,
            "seat_num": seat_num,
            "seat_num_total": seat_num_total
        }
        
        # date format not include minute if minute more than zero
        if exact_minute > 0 :
            update_kv_map['time_str'] = dt.strftime("%m{M}%d{d}%H{h}%M{m}").format(M='月', d='日', h='點', m='分')
        else :
            update_kv_map['time_str'] = dt.strftime("%m{M}%d{d}%H{h}").format(M='月', d='日', h='點')

        if seat_num_children != 0:
            update_kv_map['seat_num_children'] = seat_num_children


        ret = encapsule_rtn_format(update_kv_map, None)
        return Response(json.dumps(ret), status=200)

class SearchRestaurant(Resource):
    def post(self):
        json_from_request = json.loads(Converter('zh-hant').convert(request.stream.read().decode('utf-8')))
        user_id = json_from_request['user_id']

        text = json_from_request['text']
        date = json_from_request['task_info']['time_date']
        time = json_from_request['task_info']['time_time']
        seat_num_total = json_from_request['task_info']['seat_num_total']
        restaurant = json_from_request['task_info']['restaurant']

        # request systex
        payload = {
            "user_id": user_id,
            "text": text,
            "task_info": {                
                "date": date,
                "time": time,
                "seat_num": seat_num_total,
                "restaurant_name": restaurant
            }
        }
        r = requests.post(constants.SYSTEX_URL+'booking/searchBooking', json=payload, timeout=float(constants.REQUEST_TIMEOUT))
        r_obj = r.json()
        LOG.info(json.dumps(r_obj, ensure_ascii=False))
        
        # response
        update_kv_map = {}
        booking_status = "no_seat"
        if r_obj["msg_response"]["update"]["booking_status"] == '0':
            booking_status = "available"
        elif r_obj["msg_response"]["update"]["booking_status"] == '1':
            booking_status = "waiting_list"
            update_kv_map["waiting_order"] = r_obj["msg_response"]["update"]["waiting_order"]
        update_kv_map["restaurant_id"] = r_obj["msg_response"]["update"]["restaurant_id"]
        update_kv_map["booking_status"] = booking_status
        
        ret = encapsule_rtn_format(update_kv_map, None)
        return Response(json.dumps(ret), status=200)

class BookRestaurant(Resource):
    def post(self):
        json_from_request = json.loads(Converter('zh-hant').convert(request.stream.read().decode('utf-8')))
        user_id = json_from_request['user_id']
        text = json_from_request['text']
        date = json_from_request['task_info']['time_date']
        time = json_from_request['task_info']['time_time']
        restaurant_id = json_from_request['task_info']['restaurant_id']
        seat_num_total = json_from_request['task_info']['seat_num_total']
        lastname = json_from_request['task_info']['lastname']
        phone = json_from_request['task_info']['phone']
        
        # request
        payload = {
            "user_id": user_id,
            "text": text,
            "task_info": {
                "date": date,
                "time": time,
                "restaurant_id": restaurant_id,
                "seat_num": seat_num_total,
                "lastname": lastname,
                "phone": phone
            }
        }
        r = requests.post(constants.SYSTEX_URL+'booking/doBooking', json=payload, timeout=float(constants.REQUEST_TIMEOUT))
        r_obj = r.json()
        
        # response
        update_kv_map = {}
        booking_status = "no_seat"
        if r_obj["msg_response"]["update"]["booking_status"] == '0':
            booking_status = "available"
        elif r_obj["msg_response"]["update"]["booking_status"] == '1':
            booking_status = "waiting_list"
            update_kv_map["waiting_order"] = r_obj["msg_response"]["update"]["waiting_order"]
        update_kv_map["restaurant_id"] = r_obj["msg_response"]["update"]["restaurant_id"]
        update_kv_map["booking_status"] = booking_status
        update_kv_map["booking_id"] = r_obj["msg_response"]["update"]["id"]
        
        ret = encapsule_rtn_format(update_kv_map, None)
        return Response(json.dumps(ret), status=200)

class ResetParams(Resource):
    def post(self):
        json_from_request = json.loads(Converter('zh-hant').convert(request.stream.read().decode('utf-8')))

        # print the format of json
        LOG.debug('In ResetParams, data received from TE: %s' % json.dumps(json_from_request, ensure_ascii=False, indent=4))

        task_info = json_from_request['task_info']
        LOG.info(json.dumps(task_info, ensure_ascii=False))
        remove_kv_map = {}
        if 'seat_num' not in task_info:
            remove_kv_map["seat_num_children"] = None
        if 'phone' not in task_info:
            remove_kv_map["phone"] = None
        if 'lastname' not in task_info:
            remove_kv_map["lastname"] = None
        if 'time_str' not in task_info:
            remove_kv_map["exact_date"] = None
            remove_kv_map["exact_hour"] = None
        ret = encapsule_rtn_format(None, remove_kv_map)
        return Response(json.dumps(ret), status=200)
        
