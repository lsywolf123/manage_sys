# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
import exception
import user
import datetime
import random
from db import api as db


# 生成消费信息
def general_consume_info(merchant_id, goods_serial_num, consumer_name, consumer_phone, consume_money, consume_content, serial_num):
    goods = db.goods_get_by_serial_num(merchant_id, goods_serial_num)
    if not goods:
        raise exception.GoodsIsNotExistException()
    if goods['stock'] == 0:
        raise exception.GoodsIsNotEnoughException()
    real_consume_money = consume_money
    values = {
        'merchant_id': merchant_id,
        'consumer_name': consumer_name,
        'consume_money': consume_money,
        'consumer_phone': consumer_phone,
        'goods_id': goods['id'],
        'multiple': 1.0
    }
    if consume_content:
        values['consume_content'] = consume_content
    if serial_num:
        recomender = db.customer_get_by_serial_num(serial_num)
        if not recomender:
            raise exception.SerialNumIsNotExist()
        if not recomender['name']:
            raise exception.SerialNumIsNotBind()
        values['customer_id'] = recomender['id']
        activity = db.activity_get_by_merchant_id(merchant_id)
        now = datetime.datetime.now()
        if now > activity['start_time'] and now < activity['end_time']:
            consume_money = int(consume_money) * activity['multiple']
            values['multiple'] = activity['multiple']
        recomender_values = {
            'gb': recomender['gb'] + int(consume_money),
            'total_gb': recomender['total_gb'] + int(consume_money),
            'consume_gb': recomender['consume_gb'] + int(consume_money),
            'qualification_gb': recomender['qualification_gb'] + int(real_consume_money)
        }
        db.customer_update_by_id(recomender['id'], recomender_values)
    goods_values = {}
    goods_values['stock'] = goods['stock'] - 1
    goods_values['sales_amount'] = goods['sales_amount'] + 1
    db.goods_update_by_id(goods['id'], goods_values)
    return db.consume_create(values)


# 消费数量
def consume_count_by_id(merchant_id):
    return db.consume_count_by_merchant_id(merchant_id)


# 消费列表
def consume_list_by_merchant_id(merchant_id, page):
    consume_count = db.consume_count_by_merchant_id(merchant_id)
    page_num = consume_count/10 + 1 if consume_count % 10 else consume_count/10
    if page < 1 or page > page_num:
        return []
    temp = db.consume_list_by_merchant_id(merchant_id)
    consume_list = []
    count = 1
    for consume in temp[10*(page-1):10*page]:
        consume_dict = dict(consume)
        consume_dict['num'] = count + 10*(page-1)
        goods = db.goods_get_by_id(consume['goods_id'])
        if not goods:
            continue
        else:
            consume_dict['goods_name'] = goods['name']+'('+goods['serial_num']+')'
        if consume_dict['customer_id']:
            recomender = db.customer_get_by_id(consume_dict['customer_id'])
            consume_dict['recomender'] = recomender['name']
        else:
            consume_dict['recomender'] = '无'
        consume_dict['consume_content'] = consume_dict['consume_content'] if consume_dict['consume_content'] else '无'
        consume_list.append(consume_dict)
        count += 1
    return consume_list


# 被查询消费数量
def search_consume_count(merchant_id, type, content):
    if type == '0':
        return db.search_consume_count_by_consumer_name(merchant_id, content)
    elif type == '1':
        customer = db.customer_get_by_serial_num(content)
        if not customer:
            return 0
        return db.search_consume_count_by_customer_id(merchant_id, customer['id'])
    elif type == '2':
        min_time = content + ' 00:00:00'
        max_time = content + ' 23:59:59'
        return db.search_consume_count_by_created_at(merchant_id, min_time, max_time)


# 被查询消费列表
def get_search_consume_list(merchant_id, page, type, content):
    consume_count = search_consume_count(merchant_id, type, content)
    if type == '0':
        temp = db.consume_list_by_consumer_name(merchant_id, content)
    elif type == '1':
        customer = db.customer_get_by_serial_num(content)
        if not customer:
            return []
        temp = db.consume_list_by_customer_id(merchant_id, customer['id'])
    elif type == '2':
        min_time = content + ' 00:00:00'
        max_time = content + ' 23:59:59'
        temp = db.consume_list_by_created_at(merchant_id, min_time, max_time)
    page_num = consume_count/10 + 1 if consume_count % 10 else consume_count/10
    if page < 1 or page > page_num:
        return []
    count = 1
    consume_list = []
    for consume in temp[10*(page-1):10*page]:
        consume_dict = dict(consume)
        consume_dict['num'] = count + 10*(page-1)
        goods = db.goods_get_by_id(consume['goods_id'])
        if not goods:
            continue
        consume_dict['goods_name'] = goods['name']+'('+goods['serial_num']+')'
        if consume_dict['customer_id']:
            recomender = db.customer_get_by_id(consume_dict['customer_id'])
            consume_dict['recomender'] = recomender['name']
        else:
            consume_dict['recomender'] = '无'
        consume_dict['consume_content'] = consume_dict['consume_content'] if consume_dict['consume_content'] else '无'
        consume_list.append(consume_dict)
        count += 1
    return consume_list


# 根据会员查找消费记录
def consume_list_by_customer_id(merchant_id, customer_id):
    temp = db.consume_list_by_customer_id(merchant_id, customer_id)
    consume_list = []
    count = 1
    for consume in temp:
        consume_dict = dict(consume)
        if consume_dict['goods_id'] == u'0':
            consume_dict['consumer_name'] = '商家赠送'
        consume_dict['num'] = count
        consume_list.append(consume_dict)
        count += 1
    return consume_list


# 根据会员查找消费记录
def consume_get_by_customer_id(customer_id):
    temp = db.consume_get_by_customer_id(customer_id)
    consume_list = []
    count = 1
    for consume in temp:
        consume_dict = dict(consume)
        if consume_dict['goods_id'] == u'0':
            consume_dict['consumer_name'] = '商家赠送'
        consume_dict['num'] = count
        consume_list.append(consume_dict)
        count += 1
    return consume_list


# 根据会员查找近期消费记录
def recent_consume_list_by_customer_id(customer_id):
    temp = db.consume_recent_list_by_customer_id(customer_id)
    consume_list = []
    count = 1
    for consume in temp:
        consume_dict = dict(consume)
        consume_dict['num'] = count
        consume_list.append(consume_dict)
        count += 1
    return consume_list


# 根据会员查找消费记录
def consume_all_list_by_customer_id(customer_id):
    temp = db.consume_all_list_by_customer_id(customer_id)
    consume_list = []
    count = 1
    for consume in temp:
        consume_dict = dict(consume)
        consume_dict['num'] = count
        consume_list.append(consume_dict)
        count += 1
    return consume_list


# 消费明细
def merchant_account_book(merchant_id, year, month):
    min_time = str(year) + '-' + str(month) + '-01 00:00:00'
    max_time = str(year) + '-' +  str(month) + '-31 23:59:59'
    consume_list = db.consume_list_by_created_at(merchant_id, min_time, max_time)
    goods_list = []
    data_list = []
    total_sale_num = 0
    total_sale_money = 0
    total_profit = 0
    for consume in consume_list:
        goods = db.goods_get_by_id(consume['goods_id'])
        if not goods:
            continue
        total_sale_num += 1
        total_sale_money += consume['consume_money']
        total_profit += consume['consume_money'] - goods['price']
        if goods['serial_num'] not in goods_list:
            data_dict = {
                'goods_serial_num': goods['serial_num'],
                'goods_name': goods['name'],
                'sale_num': 1,
                'sale_money': consume['consume_money'],
                'profit': consume['consume_money'] - goods['price']
            }
            goods_list.append(goods['serial_num'])
            data_list.append(data_dict)
        else:
            data_list[goods_list.index(goods['serial_num'])]['sale_num'] += 1
            data_list[goods_list.index(goods['serial_num'])]['sale_money'] += consume['consume_money']
            data_list[goods_list.index(goods['serial_num'])]['profit'] += (consume['consume_money'] - goods['price'])
    total_statistic = {
        'goods_serial_num': '总计',
        'goods_name': '',
        'sale_num': total_sale_num,
        'sale_money': total_sale_money,
        'profit': total_profit
    }
    data_list.append(total_statistic)
    return data_list


#随机生成姓名
def general_name():
    xing = u'赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜'
    ming = u'豫章故郡洪都新府星分翼轸地接衡庐襟三江而带五湖'
    X = random.choice(xing)
    M = "".join(random.choice(ming) for i in range(2))
    return (X + M)


def general_time():
    import time
    a1 = (2017, 1, 1, 0, 0, 0, 0, 0, 0)  # 设置开始日期时间元组（2017-01-01 00：00：00）
    a2 = (2018, 7, 5, 23, 59, 59, 0, 0, 0)  # 设置结束日期时间元组（1990-12-31 23：59：59）
    start = time.mktime(a1)  # 生成开始时间戳
    end = time.mktime(a2)  # 生成结束时间戳
    # 随机生成10个日期字符串
    t = random.randint(start, end)  # 在开始和结束时间戳中随机取出一个
    date_touple = time.localtime(t)  # 将时间戳生成时间元组
    date = time.strftime("%Y-%m-%d %H:%M:%S", date_touple)
    return date


if __name__ == '__main__':
    merchant_id = '0cb0a34f-6d89-11e8-8d21-3497f688d3c6'
    goods_serial_num_list = ['FPG3649A-F','F1E9022C','FC010A18-1','F3C9022C','FL25P42','FL23L31-1','FL18D42A','FL23S31-1','FV017H','FW026Q','FC097A18-1']
    for i in range(500):
        goods = db.goods_get_by_serial_num(merchant_id, goods_serial_num_list[random.randint(0, 10)])
        values = {
            'merchant_id': merchant_id,
            'consumer_name': general_name(),
            'consume_money': random.randint(goods['price'], goods['price'] + 3000),
            'consumer_phone': '158' + str(random.randint(10000000, 19999999)),
            'goods_id': goods['id'],
            'multiple': 1.0,
            'created_at': general_time()
        }
        db.consume_create(values)
        print i