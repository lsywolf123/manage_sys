# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
import exception
import user
import datetime
import random
from db import api as db


# 会员信息
def customer_info(customer_id):
    return dict(db.customer_get_by_id(customer_id))


# 根据user_id查询会员
def get_customer_by_user_id(user_id):
    return dict(db.customer_get_by_user_id(user_id))


# 积分明细条数
def customer_gb_datail_count(customer_id):
    return db.consume_count_by_customer_id(customer_id) + db.exchange_count_by_customer_id(customer_id)


# 积分明细列表
def get_customer_gb_datail_list(customer_id, page):
    gb_datail_count = customer_gb_datail_count(customer_id)
    page_num = gb_datail_count/10 + 1 if gb_datail_count % 10 else gb_datail_count/10
    if page < 1 or page > page_num:
        return []
    gb_detail_list = []
    consume_list = db.consume_all_list_by_customer_id(customer_id)
    exchange_list = db.exchange_get_all_by_customer_id(customer_id)
    for i in range(gb_datail_count):
        gb_datail_dict = {}
        gb_datail_dict['num'] = i + 1
        if len(consume_list) == 0:
            gb_datail_dict['object'] =  exchange_list[0]['customer_name']
            gb_datail_dict['type'] = '消费积分'
            gb_datail_dict['result'] = -exchange_list[0]['exchange_goldbean']
            gb_datail_dict['money'] = exchange_list[0]['exchange_money']
            gb_datail_dict['created_at'] = exchange_list[0]['created_at']
            exchange_list.pop(0)
            gb_detail_list.append(gb_datail_dict)
            continue
        if len(exchange_list) == 0:
            gb_datail_dict['object'] = consume_list[0]['consumer_name']
            gb_datail_dict['type'] = '获取积分'
            gb_datail_dict['result'] = int(consume_list[0]['consume_money'] * consume_list[0]['multiple'])
            gb_datail_dict['money'] = 0
            gb_datail_dict['created_at'] = consume_list[0]['created_at']
            consume_list.pop(0)
            gb_detail_list.append(gb_datail_dict)
            continue
        if consume_list[0]['created_at'] >= exchange_list[0]['created_at']:
            gb_datail_dict['object'] = consume_list[0]['consumer_name']
            gb_datail_dict['type'] = '获取积分'
            gb_datail_dict['result'] = int(consume_list[0]['consume_money'] * consume_list[0]['multiple'])
            gb_datail_dict['money'] = 0
            gb_datail_dict['created_at'] = consume_list[0]['created_at']
            consume_list.pop(0)
            gb_detail_list.append(gb_datail_dict)
            continue
        else:
            gb_datail_dict['object'] =  exchange_list[0]['customer_name']
            gb_datail_dict['type'] = '消费积分'
            gb_datail_dict['result'] = -exchange_list[0]['exchange_goldbean']
            gb_datail_dict['money'] = exchange_list[0]['exchange_money']
            gb_datail_dict['created_at'] = exchange_list[0]['created_at']
            exchange_list.pop(0)
            gb_detail_list.append(gb_datail_dict)
            continue
    return gb_detail_list[10*(page-1):10*page]


# 根据customer_id查找活动
def gb_activity_by_customer_id(customer_id):
    merchant_id = db.customer_get_by_id(customer_id)['merchant_id']
    result = db.activity_get_by_merchant_id(merchant_id)
    activity_dict = dict(result) if result else {'multiple': '***', 'start_time': '***', 'end_time': '***'}
    return activity_dict


# 根据customer_id更新会员基本信息
def customer_update_by_customer_id(customer_id, phone, email, we_chat):
    values = {
        'phone': phone,
        'email': email,
        'we_chat': we_chat,
    }
    return db.customer_update_by_id(customer_id, values)


if __name__ == "__main__":
    for i in get_customer_gb_datail_list('a4cb2611-680d-11e7-8161-3497f688d3c6', 1):
        print i