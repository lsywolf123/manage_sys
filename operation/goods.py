# -*- coding: utf-8 -*-
# Created on 2018-7-3
# @author: lsy
import exception
from db import api as db


# 创建新用户
def create_goods(merchant_id, name, serial_num, price, offer, stock):
    if db.goods_if_exist_in_db(merchant_id, serial_num):
        raise exception.GoodsIsExistException()
    values = {
        'merchant_id': merchant_id,
        'name': name,
        'serial_num': serial_num,
        'price': price,
        'offer': offer,
        'stock': stock,
    }
    return db.goods_create(values)


# 修改商品
def update_goods(goods_id, name, serial_num, price, offer, stock):
    values = {}
    if name:
        values['name'] = name
    if serial_num:
        values['serial_num'] = serial_num
    if price:
        values['price'] = price
    if offer:
        values['offer'] = offer
    if stock:
        values['stock'] = stock
    return db.goods_update_by_id(goods_id, values)


# 删除商品
def goods_delete_by_id(goods_id):
    return db.goods_delete_by_id(goods_id)


# 根据id查询商品
def goods_get_by_id(goods_id):
    goods_dict = dict(db.goods_get_by_id(goods_id))
    return goods_dict


# 商品总数量
def goods_count(merchant_id):
    return db.goods_count(merchant_id)


# 被查询商品数量
def search_goods_count(merchant_id, type, content):
    if type == '0':
        return db.search_goods_count_by_serial_num(merchant_id, content)
    elif type == '1':
        return db.search_goods_count_by_name(merchant_id, content)
    elif type == '2':
        min_gb = int(content) * 5
        max_gb = int(content) * 5 + 5 if content != '3'else 1000000000
        return db.search_goods_count_by_stock_range(merchant_id, min_gb, max_gb)


# 商品列表
def get_goods_list(merchant_id, page):
    goods_count = db.goods_count(merchant_id)
    page_num = goods_count / 10 + 1 if goods_count % 10 else goods_count / 10
    if page < 1 or page > page_num:
        return []
    temp = db.goods_list_asc(merchant_id)
    count = 1
    goods_list = []
    for goods in temp:
        values = dict(goods)
        values['num'] = count
        values['profit'] = goods['offer'] - goods['price']
        goods_list.append(values)
        count += 1
    return goods_list[10 * (page - 1):10 * page]


# 被查询商品列表
def get_search_goods_list(merchant_id, page, type, content):
    if type == '0':
        search_goods_count = db.search_goods_count_by_serial_num(merchant_id, content)
        temp = db.goods_list_by_serial_num_asc(merchant_id, content)
    elif type == '1':
        search_goods_count = db.search_goods_count_by_name(merchant_id, content)
        temp = db.goods_list_by_name_asc(merchant_id, content)
    elif type == '2':
        min_gb = int(content) * 5
        max_gb = int(content) * 5 + 5 if content != '3'else 1000000000
        search_goods_count = db.search_goods_count_by_stock_range(merchant_id, min_gb, max_gb)
        temp = db.goods_list_by_stock_asc(merchant_id, min_gb, max_gb)
    page_num = search_goods_count/10 + 1 if search_goods_count % 10 else search_goods_count/10
    if page < 1 or page > page_num:
        return []
    count = 1
    goods_list = []
    for goods in temp:
        values = dict(goods)
        values['num'] = count
        values['profit'] = goods['offer'] - goods['price']
        goods_list.append(values)
        count += 1
    return goods_list[10*(page-1):10*page]