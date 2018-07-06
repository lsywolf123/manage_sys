# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
import time
from base import BaseHandler
from tornado.web import authenticated
from operation import goods, manager


def now():
    return time.strftime("%Y-%m-%d", time.localtime())


class GoodsListHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '2':
            self.redirect('/index')
        page = self.get_argument('page')
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        type = self.get_argument('type')
        content = self.get_argument('content')
        if type and content:
            goods_count = goods.search_goods_count(merchant_id, type, content)
            page_num = goods_count / 10 + 1 if goods_count % 10 else goods_count / 10
            goods_list = goods.get_search_goods_list(merchant_id, 1, type, content)
        else:
            goods_count = goods.goods_count(merchant_id)
            page_num = goods_count/10 + 1 if goods_count % 10 else goods_count/10
            goods_list = goods.get_goods_list(merchant_id, int(page))
        info = {'page_num': page_num,
                'goods_list': goods_list,
                'page': int(page),
                'username': username,
                'type': type,
                'content': content,
                }
        self.render('merchant-goods-list.html', **info)

    def post(self):
        type = self.get_argument('type')
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        content = self.get_argument('content%s'%type)
        search_goods_count = goods.search_goods_count(merchant_id, type, content)
        page_num = search_goods_count / 10 + 1 if search_goods_count % 10 else search_goods_count / 10
        search_goods_list = goods.get_search_goods_list(merchant_id, 1, type, content)
        info = {'page_num': page_num,
                'goods_list': search_goods_list,
                'page': 1,
                'username': username,
                'type': type,
                'content': content
                }
        self.render('merchant-goods-list.html', **info)


class AddGoodsHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '2':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        self.render('merchant-add-goods.html', username=username, message = '')

    def post(self):
        message = None
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        serial_num = self.get_argument('serial_num')
        name = self.get_argument('name')
        price = self.get_argument('price')
        offer = self.get_argument('offer')
        stock = self.get_argument('stock')
        if not serial_num:
            message = '商品编号为必填项'
        elif not name:
            message = '商品名字为必填项'
        elif not price:
            message = '商品价格为必填项'
        elif not offer:
            message = '商品报价为必填项'
        elif not stock:
            message = '商品库存为必填项'
        if message:
            self.render('merchant-add-goods.html', username=username, message=message, name=name, serial_num=serial_num, price=price,
                        offer=offer, stock=stock)
            return
        try:
            ref = goods.create_goods(merchant_id, name, serial_num, price, offer, stock)
        except Exception as e:
            err_msg = e.message
            self.render('merchant-add-goods.html',username=username, message=err_msg, name=name, serial_num=serial_num, price=price,
                        offer=offer, stock=stock)
            return
        if ref:
            self.render('merchant-add-goods.html', username=username, message='添加成功',  name='', serial_num='',
                        price='', offer='', stock='')


class UpdategoodsHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '2':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        goods_id = self.get_argument('id')
        goods_info = goods.goods_get_by_id(goods_id)
        self.render('merchant-update-goods.html', username=username, message='', id=goods_id, name=goods_info['name'],
                    serial_num=goods_info['serial_num'], price=goods_info['price'], offer=goods_info['offer'],
                    stock=goods_info['stock'])

    def post(self):
        username = self.get_secure_cookie('username')
        name = self.get_argument('name')
        serial_num = self.get_argument('serial_num')
        price = self.get_argument('price')
        offer = self.get_argument('offer')
        stock = self.get_argument('stock')
        goods_id = self.get_argument('id')
        try:
            ref = goods.update_goods(goods_id, name, serial_num, price, offer, stock)
        except Exception as e:
            err_msg = e.message
            self.render('merchant-update-goods.html', username=username, message=err_msg, id=goods_id, name=name,
                        serial_num=serial_num, price=price, offer=offer, stock=stock)
            return
        if ref:
            self.render('merchant-update-goods.html', username=username, message='修改成功', id=goods_id, name=ref['name'],
                        serial_num=ref['serial_num'], price=ref['price'], offer=ref['offer'], stock=ref['stock'])


class DeleteGoodsHandle(BaseHandler):
    @authenticated
    def post(self):
        if self.get_secure_cookie('role') != '1':
            self.redirect('/index')
        goods_id = self.get_argument('id')
        ref = goods.goods_delete_by_id(goods_id)
        if ref:
            self.redirect('//merchant-goods-list?page=1')
#
#
# class AddCustomerHandle(BaseHandler):
#     @authenticated
#     def get(self):
#         if self.get_secure_cookie('role') != '1':
#             self.redirect('/index')
#         username = self.get_secure_cookie('username')
#         self.render('manager-add-customer.html', username=username, start_num='', end_num='', message='')
#
#     def post(self):
#         message = None
#         username = self.get_secure_cookie('username')
#         start_num = self.get_argument('start_num')
#         end_num = self.get_argument('end_num')
#         password = self.get_argument('password')
#         user_ref = user.get_user_by_username(username)
#         if password != user_ref['password']:
#             message = '密码错误'
#         if not start_num:
#             message = '起始编号为必填项'
#         if not end_num:
#             message = '结束编号为必填项'
#         try:
#             if int(start_num) < 0:
#                 message = '起始编号必须为大于0的数字'
#             if int(end_num) < 0:
#                 message = '结束编号必须为大于0的数字'
#             if int(start_num) > int(end_num):
#                 message = '结束编号必须不小于起始编号'
#         except:
#             message = '编号必须是数字'
#         if not password:
#             message = '密码为必填项'
#         if message:
#             self.render('manager-add-customer.html', username=username, start_num='', end_num='', message=message)
#             return
#         try:
#             ref = manager.add_customer(int(start_num), int(end_num))
#         except Exception as e:
#             self.render('manager-add-customer.html', username=username, start_num='', end_num='', message=e.message)
#             return
#         if ref:
#             self.render('manager-add-customer.html', username=username, start_num='', end_num='', message='添加成功')
#             return
#
#
# class CustomerAddedListHandle(BaseHandler):
#     def get(self):
#         if self.get_secure_cookie('role') != '1':
#             self.redirect('/index')
#         username = self.get_secure_cookie('username')
#         page = self.get_argument('page')
#         result = manager.get_added_customer_list(int(page))
#         added_customer_list = result[0]
#         page_num = result[1]
#         info = {'page_num': page_num,
#                 'added_customer_list': added_customer_list,
#                 'page': int(page),
#                 'username': username
#                 }
#         self.render('manager-add-customer-list.html', **info)
#
#
# class CustomerAddedInfoHandle(BaseHandler):
#     def get(self):
#         if self.get_secure_cookie('role') != '1':
#             self.redirect('/index')
#         username = self.get_secure_cookie('username')
#         page = self.get_argument('page')
#         created_time = self.get_argument('created_time')
#         added_customer_info_list = manager.get_added_customer_info(created_time, int(page))
#         added_customer_info_count = manager.get_add_customer_info_count(created_time)
#         page_num = added_customer_info_count / 10 + 1 if added_customer_info_count % 10 else added_customer_info_count / 10
#         info = {'page_num': page_num,
#                 'added_customer_info_list': added_customer_info_list,
#                 'page': int(page),
#                 'username': username,
#                 'created_time': created_time
#                 }
#         self.render('manager-add-customer-info.html', **info)
#
#
# class CustomerListHandle(BaseHandler):
#     @authenticated
#     def get(self):
#         if self.get_secure_cookie('role') != '1':
#             self.redirect('/index')
#         type = self.get_argument('type')
#         content = self.get_argument('content')
#         page = self.get_argument('page')
#         username = self.get_secure_cookie('username')
#         if type and content:
#             customer_count = manager.search_customer_count(type, content)
#             page_num = customer_count / 10 + 1 if customer_count % 10 else customer_count / 10
#             customer_list = manager.get_search_customer_list(int(page), type, content)
#         else:
#             customer_count = manager.customer_count()
#             page_num = customer_count/10 + 1 if customer_count % 10 else customer_count/10
#             customer_list = manager.customer_list(int(page))
#         info = {'type': type,
#                 'content': content,
#                 'page_num': page_num,
#                 'customer_list': customer_list,
#                 'page': int(page),
#                 'username': username
#                 }
#         self.render('manager-customers.html', **info)
#
#     def post(self):
#         type = self.get_argument('type')
#         username = self.get_secure_cookie('username')
#         content = self.get_argument('content%s'%type)
#         customer_count = manager.search_customer_count(type, content)
#         page_num = customer_count / 10 + 1 if customer_count % 10 else customer_count / 10
#         customer_list = manager.get_search_customer_list(1, type, content)
#         info = {'type': type,
#                 'content': content,
#                 'page_num': page_num,
#                 'customer_list': customer_list,
#                 'page': 1,
#                 'username': username
#                 }
#         self.render('manager-customers.html', **info)
#
#
# class ManagerCustomerInfoHandle(BaseHandler):
#     @authenticated
#     def get(self):
#         if self.get_secure_cookie('role') != '1':
#             self.redirect('/index')
#         username = self.get_secure_cookie('username')
#         customer_id = self.get_argument('customer_id')
#         customer_info = customer.customer_info(customer_id)
#         consume_list = consume.consume_all_list_by_customer_id(customer_id)
#         info = {'customer_info': customer_info,
#                 'username': username,
#                 'consume_list': consume_list
#                 }
#         self.render('manager-customer-info.html', **info)
