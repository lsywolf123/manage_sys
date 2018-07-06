# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
import exception
import user
import datetime
import random
from db import api as db


# 把datetime转成字符串
def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d")


# 随机生成六位数
def general_num():
    num = ''
    for i in range(6):
        a = random.randint(1, 7)
        num = num + str(a)
    return num


# 添加商户
def add_merchant(name, host_name, phone, email, address, deadline, password='123456'):
    if db.merchant_phone_if_exist_in_db(phone):
        raise exception.PhoneIsExistException()
    values = {
        'name': name,
        'host_name': host_name,
        'phone': phone,
        'email': email,
        'address': address,
        'deadline': deadline,
    }
    ref = user.create_user(phone, password, '2')
    values['user_id'] = ref['id']
    ref = db.merchant_create(values)
    values = {
        'merchant_id': ref['id'],
        'level1': 100,
        'level2': 240,
        'level3': 408,
        'level4': 608,
        'level5': 858,
        'level6': 1138,
        'level7': 1498,
        'level8': 2028,
        'rule_info': '推荐贵宾在****消费，每消费1元推荐者活动1积分，以5000进度为起点，会员可以自选档次兑换感'
                     '恩回馈金。（活动期间：参加活动的会员介绍消费成功可按活动期间倍率来获取积分）'
    }
    db.rule_create(values)
    values = {
        'merchant_id': ref['id'],
        'multiple': 2,
        'start_time': datetime_toString(datetime.datetime.now() - datetime.timedelta(days=1)),
        'end_time': datetime_toString(datetime.datetime.now())
    }
    db.activity_create(values)
    return ref


# 添加会员
def add_customer(start_num, end_num):
    now = datetime.datetime.now()
    for i in range(end_num - start_num + 1):
        values = {
            'serial_num': start_num + i
        }
        ref = user.create_user(values['serial_num'], general_num(), '3', now)
        values['user_id'] = ref['id']
        values['created_at'] = now
        db.customer_create(values)
    return True


# 修改商户
def update_merchant(merchant_id, name, host_name, phone, email, address, deadline):
    values = {}
    if name:
        values['name'] = name
    if host_name:
        values['host_name'] = host_name
    if host_name:
        values['phone'] = phone
    if host_name:
        values['email'] = email
    if host_name:
        values['address'] = address
    if host_name:
        values['deadline'] = deadline
    return db.merchant_update_by_id(merchant_id, values)


# 删除商户
def merchant_delete_by_id(merchant_id):
    return db.merchant_delete_by_id(merchant_id)


# 商户列表
def get_merchant_list(page):
    merchant_count = db.merchant_count()
    page_num = merchant_count/10 + 1 if merchant_count % 10 else merchant_count/10
    if page < 1 or page > page_num:
        return []
    temp = db.merchant_list_asc()
    count = 1
    merchant_list = []
    for merchant in temp:
        values = dict(merchant)
        values['num'] = count
        values['status'] = True if datetime_toString(datetime.datetime.now()) < datetime_toString(values['deadline']) else False
        merchant_list.append(values)
        count += 1
    return merchant_list[10*(page-1):10*page]


# 新增会员列表
def get_added_customer_list(page):
    temp = db.customer_added_list()
    group_time = None
    added_customer_list = []
    count = 1
    for customer in temp:
        if group_time != customer['created_at']:
            group_time = customer['created_at']
            group_customer_dict = {'count': 0,
                                   'created_time': group_time,
                                   'group_start_num': customer['username'],
                                   'num': count}
            count += 1
            added_customer_list.append(group_customer_dict)
        group_customer_dict['count'] += 1
    page_num = len(added_customer_list)/10 + 1 if len(added_customer_list) % 10 else len(added_customer_list)/10
    if page < 1 or page > page_num:
        return []
    return added_customer_list[10*(page-1):10*page], page_num


# 新增会员详细信息
def get_added_customer_info(created_time, page):
    temp = db.customer_added_list_by_created_time(created_time)
    added_customer_info_list = []
    num = 1 + 10 * (page - 1)
    for user in temp[10*(page-1):10*page]:
        customer_dict = dict(db.customer_get_by_serial_num(user['username']))
        user = db.user_get_by_id(customer_dict['user_id'])
        customer_dict['password'] = user['password']
        customer_dict['num'] = num
        added_customer_info_list.append(customer_dict)
        num += 1
    page_num = len(temp) / 10 + 1 if len(temp) % 10 else len(temp) / 10
    if page < 1 or page > page_num:
        return []
    return added_customer_info_list


# 新增会员详细信息数量
def get_add_customer_info_count(created_time):
    return db.customer_added_count_by_created_time(created_time)


# 被查询商户列表
def get_search_merchant_list(page, type, content):
    if type == '0':
        search_merchant_count = db.search_merchant_count_by_name(content)
        temp = db.merchant_list_by_name_asc(content)
    elif type == '1':
        search_merchant_count = db.search_merchant_count_by_hostname(content)
        temp = db.merchant_list_by_hostname_asc(content)
    elif type == '2':
        search_merchant_count = db.search_merchant_count_by_phone(content)
        temp = db.merchant_list_by_phone_asc(content)
    page_num = search_merchant_count/10 + 1 if search_merchant_count % 10 else search_merchant_count/10
    if page < 1 or page > page_num:
        return []
    count = 1
    merchant_list = []
    for merchant in temp:
        values = dict(merchant)
        values['num'] = count
        values['status'] = True if datetime_toString(datetime.datetime.now()) < datetime_toString(values['deadline']) else False
        merchant_list.append(values)
        count += 1
    return merchant_list[10*(page-1):10*page]


# 根据id查询商户
def merchant_get_by_id(merchant_id):
    merchant_dict = dict(db.merchant_get_by_id(merchant_id))
    merchant_dict['deadline'] = datetime_toString(merchant_dict['deadline'])
    return merchant_dict


# 商户总数量
def merchant_count():
    return db.merchant_count()


# 被查询商户数量
def search_merchant_count(type, content):
    if type == '0':
        return db.search_merchant_count_by_name(content)
    elif type == '1':
        return db.search_merchant_count_by_hostname(content)
    elif type == '2':
        return db.search_merchant_count_by_phone(content)


# 商户过期数量
def merchant_expire_count():
    return db.merchant_expire_count()


# 会员总数量
def customer_count():
    return db.customer_count()


# 活跃会员数量
def customer_active_count():
    return db.customer_active_count()


# 最近入驻商户信息
def recent_merchant_list():
    temp = db.merchant_recent_list()
    merchant_list = []
    for merchant in temp:
        merchant_dict = dict(merchant)
        merchant_list.append(merchant_dict)
    return merchant_list


# 最近入驻商户数量
def recent_merchant_count():
    return db.merchant_recent_count()


# 最近入驻会员户信息
def recent_customer_list():
    temp = db.customer_recent_list()
    customer_list = []
    for customer in temp:
        customer_dict = dict(customer)
        merchant = db.merchant_get_by_id(customer_dict['merchant_id'])
        customer_dict['merchant_name'] = merchant['name']
        customer_list.append(customer_dict)
    return customer_list


# 最近入驻会员数量
def recent_customer_count():
    return db.customer_recent_count()


# 会员列表
def customer_list(page):
    count = db.customer_count()
    page_num = count/10 + 1 if count % 10 else count/10
    if page < 1 or page > page_num:
        return []
    temp = db.customer_list()
    c_list = []
    count = 1
    for customer in temp:
        c_dict = dict(customer)
        c_dict['num'] = count
        merchant_id = customer['merchant_id']
        merchant = db.merchant_get_by_id(merchant_id)
        if merchant:
            c_dict['merchant'] = merchant['name']
            c_list.append(c_dict)
            count += 1
    return c_list[10*(page-1):10*page]


# 被查询会员数量
def search_customer_count(type, content):
    if type == '0':
        return db.search_all_customer_count_by_serial_num(content)
    elif type == '1':
        return db.search_all_customer_count_by_name(content)
    elif type == '2':
        return db.search_all_customer_count_by_phone(content)
    elif type == '3':
        min_gb = int(content) * 5000
        max_gb = int(content) * 5000 + 5000 if content != '8'else 1000000000
        return db.search_all_customer_count_by_gb_range(min_gb, max_gb)
    elif type == '4':
        merchant = db.merchant_get_by_name(content)
        return db.search_all_customer_count_by_merchant_id(merchant['id'])



# 被查询会员列表
def get_search_customer_list(page, type, content):
    count = search_customer_count(type, content)
    if type == '0':
        temp = db.customer_all_list_by_serial_num(content)
    elif type == '1':
        temp = db.customer_all_list_by_name(content)
    elif type == '2':
        temp = db.customer_all_list_by_phone(content)
    elif type == '3':
        min_gb = int(content) * 5000
        max_gb = int(content) * 5000 + 5000 if content != '8'else 1000000000
        temp = db.customer_all_list_by_gb_range(min_gb, max_gb)
    elif type == '4':
        merchant = db.merchant_get_by_name(content)
        temp = db.customer_all_list_by_merchant_id(merchant['id'])
    page_num = count/10 + 1 if count % 10 else count/10
    if page < 1 or page > page_num:
        return []
    count = 1
    c_list = []
    for customer in temp:
        values = dict(customer)
        values['num'] = count
        merchant_id = customer['merchant_id']
        merchant = db.merchant_get_by_id(merchant_id)
        if merchant:
            values['merchant'] = merchant['name']
            c_list.append(values)
            count += 1
    return c_list[10*(page-1):10*page]


if __name__ == '__main__':
    values = {
        'merchant_id': 'b8e889de-67ad-11e7-a1d0-3497f688d3c6',
        'multiple': 2,
        'start_time': datetime_toString(datetime.datetime.now() - datetime.timedelta(days=1)),
        'end_time': datetime_toString(datetime.datetime.now())
    }
    db.activity_create(values)