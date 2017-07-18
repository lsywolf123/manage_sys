# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
import datetime
from base import BaseHandler
from tornado.web import authenticated
from operation import merchant
from operation import customer
from operation import consume


# 把datetime转成字符串
def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d")


class MerchantBindCustomerHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '2':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        self.render('merchant-bind.html', username=username, message='', serial_num='',
                    password='', name='', identify_id='', phone='', email='')

    def post(self):
        merchant_id = self.get_secure_cookie('merchant_id')
        username = self.get_secure_cookie('username')
        serial_num = self.get_argument('serial_num')
        password = self.get_argument('password')
        name = self.get_argument('name')
        identify_id = self.get_argument('identify_id')
        phone = self.get_argument('phone')
        email = self.get_argument('email')
        we_chat = self.get_argument('we_chat')
        message = None
        if not serial_num:
            message = '编号为必填项'
        elif not password:
            message = '密码为必填项'
        elif not name:
            '姓名为必填项'
        elif not identify_id:
            message = '身份证号为必填项'
        elif not phone:
            message = '手机号码为必填项'
        elif not email:
            message = '邮箱为必填项'
        elif not we_chat:
            message = '微信号为必填项'
        if message:
            self.render('merchant-bind.html', message=message, username=username, serial_num=serial_num,
                        password=password, name=name,identify_id=identify_id, phone=phone, email=email, we_chat=we_chat)
            return
        try:
            ref = merchant.bind_customer(merchant_id, serial_num, password, name, identify_id, phone, email, we_chat)
        except Exception as e:
            message = e.message
            self.render('merchant-bind.html', message=message, username=username, serial_num=serial_num,
                        password=password, name=name,identify_id=identify_id, phone=phone, email=email, we_chat=we_chat)
            return

        if ref:
            self.render('merchant-bind.html', message='绑定成功', username=username, serial_num=serial_num,
                        password=password, name=name,identify_id=identify_id, phone=phone, email=email, we_chat=we_chat)


class MerchantCustomerListHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '2':
            self.redirect('/index')
        type = self.get_argument('type')
        content = self.get_argument('content')
        page = self.get_argument('page')
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        if type and content:
            customer_count = merchant.search_customer_count(merchant_id, type, content)
            page_num = customer_count / 10 + 1 if customer_count % 10 else customer_count / 10
            customer_list = merchant.get_search_customer_list()
        else:
            customer_count = merchant.customer_count_by_id(merchant_id)
            page_num = customer_count/10 + 1 if customer_count % 10 else customer_count/10
            customer_list = merchant.customer_list_by_merchant_id(merchant_id, int(page))
        info = {'type': type,
                'content': content,
                'page_num': page_num,
                'customer_list': customer_list,
                'page': int(page),
                'username': username
                }
        self.render('merchant-users.html', **info)

    def post(self):
        type = self.get_argument('type')
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        content = self.get_argument('content%s'%type)
        search_customer_count = merchant.search_customer_count(merchant_id, type, content)
        page_num = search_customer_count / 10 + 1 if search_customer_count % 10 else search_customer_count / 10
        search_customer_list = merchant.get_search_customer_list(merchant_id, 1, type, content)
        info = {'type': type,
                'content': content,
                'page_num': page_num,
                'customer_list': search_customer_list,
                'page': 1,
                'username': username
                }
        self.render('merchant-users.html', **info)


class MerchantCustomerInfoHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '2':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        customer_id = self.get_argument('customer_id')
        customer_info = customer.customer_info(customer_id)
        consume_list = consume.consume_list_by_customer_id(merchant_id, customer_id)
        info = {'customer_info': customer_info,
                'username': username,
                'consume_list': consume_list
                }
        self.render('merchant-user-info.html', **info)


class MerchantCustomerConsumptHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '2':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        info = {'consume_money': '',
                'consumer_name': '',
                'consume_content': '',
                'serial_num': '',
                'username': username,
                'message': ''
                }
        self.render('merchant-user-consumpt.html', **info)

    def post(self):
        consume_money = self.get_argument('consume_money')
        consumer_name = self.get_argument('consumer_name')
        consume_content = self.get_argument('consume_content')
        serial_num = self.get_argument('serial_num')
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        message = None
        if not consume_money:
            message = '消费金额为必填项'
        elif not consumer_name:
            message = '消费人姓名为必填项'
        info = {'consume_money': consume_money,
                'consumer_name': consumer_name,
                'consume_content': consume_content,
                'serial_num': serial_num,
                'username': username,
                'message': message
                }
        if message:
            self.render('merchant-user-consumpt.html', **info)
            return
        try:
            ref = consume.general_consume_info(merchant_id, consumer_name, consume_money, consume_content, serial_num)
        except Exception as e:
            info['message'] = e.message
            self.render('merchant-user-consumpt.html', **info)
            return
        if ref:
            self.render('merchant-user-consumpt.html', consumer_name='', consume_money='', consume_content='',
                        serial_num='', username=username, message='提交成功')


class MerchantRuleHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '2':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        rule = merchant.get_merchant_rule(merchant_id)
        info = {'rule': rule,
                'username': username,
                }
        self.render('merchant-rule.html', **info)


class MerchantUpdateRuleHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '2':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        info = {
                'username': username,
                'message': ''
                }
        self.render('merchant-update-rule.html', **info)

    def post(self):
        level1 = self.get_argument('level1')
        level2 = self.get_argument('level2')
        level3 = self.get_argument('level3')
        level4 = self.get_argument('level4')
        level5 = self.get_argument('level5')
        level6 = self.get_argument('level6')
        level7 = self.get_argument('level7')
        level8 = self.get_argument('level8')
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        info = {
                'username': username,
                }
        try:
            ref = merchant.update_merchant_rule(merchant_id, level1, level2, level3, level4, level5, level6,
                                                level7, level8, '')
        except Exception as e:
            info['message'] = e.message
            self.render('merchant-update-rule.html', **info)
            return
        if ref:
            self.render('merchant-update-rule.html', username=username, message='修改成功')


class MerchantUpdateRuleInfoHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '2':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        info = {
                'username': username,
                'message': ''
                }
        self.render('merchant-update-rule-info.html', **info)

    def post(self):
        rule_info = self.get_argument('rule_info')
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        info = {
                'username': username,
                }
        try:
            ref = merchant.update_merchant_rule(merchant_id, '', '', '', '', '', '',
                                                '', '', rule_info)
        except Exception as e:
            info['message'] = e.message
            self.render('merchant-update-rule-info.html', **info)
            return
        if ref:
            self.render('merchant-update-rule-info.html', username=username, message='修改成功')


class MerchantGoldbeanHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '2':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        activity = merchant.get_merchant_activity(merchant_id)
        info = {
                'username': username,
                'activity': activity
                }
        self.render('merchant-goldbean.html', **info)


class MerchantUpdateGoldbeanHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '2':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        activity = merchant.get_merchant_activity(merchant_id)
        activity['start_time'] = datetime_toString(activity['start_time'])
        activity['end_time'] = datetime_toString(activity['end_time'])
        info = {
                'username': username,
                'activity': activity,
                'message': ''
                }
        self.render('merchant-update-goldbean.html', **info)

    def post(self):
        start_time = self.get_argument('start_time')
        end_time = self.get_argument('end_time')
        multiple = self.get_argument('multiple')
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        info = {
                'username': username,
                }
        message = None
        if not multiple:
            message = '倍数为必填项'
        elif not start_time:
            message = '开始时间为必填项'
        elif not end_time:
            message = '结束时间为必填项'
        if message:
            info['message'] = message
            self.render('merchant-update-goldbean.html', **info)
            return
        try:
            ref = merchant.update_merchant_activity(merchant_id, multiple, start_time, end_time)
        except Exception as e:
            info['message'] = e.message
            self.render('merchant-update-goldbean.html', **info)
            return
        if ref:
            info['message'] = '修改成功'
            info['activity'] = ref
            self.render('merchant-update-goldbean.html', **info)


class MerchantExchangeGoldbeanHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '2':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        exchange_ratio = merchant.get_merchant_rule(merchant_id)
        info = {'exchange_ratio': exchange_ratio,
                'username': username,
                'serial_num': '',
                'name': '',
                'identify_id': '',
                'password': '',
                'message': ''
                }
        self.render('merchant-exchange-goldbean.html', **info)

    def post(self):
        serial_num = self.get_argument('serial_num')
        name = self.get_argument('name')
        identify_id = self.get_argument('identify_id')
        password = self.get_argument('password')
        ratio = self.get_argument('ratio')
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        exchange_ratio = merchant.get_merchant_rule(merchant_id)
        info = {'exchange_ratio': exchange_ratio,
                'username': username,
                'serial_num': serial_num,
                'name': name,
                'identify_id': identify_id,
                'password': password
                }
        message = None
        if not serial_num:
            message = '客户编号为必填项'
        elif not name:
            message = '客户姓名为必填项'
        elif not identify_id:
            message = '客户身份证号为必填项'
        elif not password:
            message = '管理员密码为必填项'
        if message:
            info['message'] = message
            self.render('merchant-exchange-goldbean.html', **info)
            return
        try:
            merchant.check_password(merchant_id, password)
            ref = merchant.exchange_goldbean(merchant_id, serial_num, name, identify_id, ratio)
        except Exception as e:
            info['message'] = e.message
            self.render('merchant-exchange-goldbean.html', **info)
            return
        if ref:
            info['message'] = '兑换成功'
            self.render('merchant-exchange-goldbean.html', **info)


class MerchantConsumeListHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '2':
            self.redirect('/index')
        type = self.get_argument('type')
        content = self.get_argument('content')
        page = self.get_argument('page')
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        if type and content:
            consume_count = consume.search_consume_count(merchant_id, type, content)
            page_num = consume_count / 10 + 1 if consume_count % 10 else consume_count / 10
            consume_list = consume.get_search_consume_list(merchant_id, int(page), type, content)
        else:
            consume_count = consume.consume_count_by_id(merchant_id)
            page_num = consume_count/10 + 1 if consume_count % 10 else consume_count/10
            consume_list = consume.consume_list_by_merchant_id(merchant_id, int(page))
        info = {'type': type,
                'content': content,
                'page_num': page_num,
                'consume_list': consume_list,
                'page': int(page),
                'username': username,
                'now': datetime_toString(datetime.datetime.now())
                }
        self.render('merchant-consume-list.html', **info)

    def post(self):
        type = self.get_argument('type')
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        content = self.get_argument('content%s'%type)
        consume_count = consume.search_consume_count(merchant_id, type, content)
        page_num = consume_count / 10 + 1 if consume_count % 10 else consume_count / 10
        consume_list = consume.get_search_consume_list(merchant_id, 1, type, content)
        info = {'type': type,
                'content': content,
                'page_num': page_num,
                'consume_list': consume_list,
                'page': 1,
                'username': username,
                'now': content if content == '2' else datetime_toString(datetime.datetime.now())
                }
        self.render('merchant-consume-list.html', **info)


class MerchantExchangeListHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '2':
            self.redirect('/index')
        type = self.get_argument('type')
        content = self.get_argument('content')
        page = self.get_argument('page')
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        if type and content:
            exchange_count = merchant.search_exchange_count(merchant_id, type, content)
            page_num = exchange_count / 10 + 1 if exchange_count % 10 else exchange_count / 10
            exchange_list = merchant.get_search_exchange_list(merchant_id, int(page), type, content)
        else:
            exchange_count = merchant.exchange_count_by_id(merchant_id)
            page_num = exchange_count/10 + 1 if exchange_count % 10 else exchange_count/10
            exchange_list = merchant.exchange_list_by_merchant_id(merchant_id, int(page))
        info = {'type': type,
                'content': content,
                'page_num': page_num,
                'exchange_list': exchange_list,
                'page': int(page),
                'username': username,
                'now': datetime_toString(datetime.datetime.now())
                }
        self.render('merchant-exchange-list.html', **info)

    def post(self):
        type = self.get_argument('type')
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        content = self.get_argument('content%s'%type)
        exchange_count = merchant.search_exchange_count(merchant_id, type, content)
        page_num = exchange_count / 10 + 1 if exchange_count % 10 else exchange_count / 10
        exchange_list = merchant.get_search_exchange_list(merchant_id, 1, type, content)
        info = {'type': type,
                'content': content,
                'page_num': page_num,
                'exchange_list': exchange_list,
                'page': 1,
                'username': username,
                'now': content if content == '2' else datetime_toString(datetime.datetime.now())
                }
        self.render('merchant-exchange-list.html', **info)


class MerchantGiveGbHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '2':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        customer_id = self.get_argument('customer_id')
        self.render('merchant-give-goldbean.html', username=username, customer_id=customer_id, message='', gb_num='', password='')

    def post(self):
        merchant_id = self.get_secure_cookie('merchant_id')
        username = self.get_secure_cookie('username')
        customer_id = self.get_argument('customer_id')
        gb_num = self.get_argument('gb_num')
        password = self.get_argument('password')
        message = None
        if not gb_num:
            message = '赠豆数量为必填项'
        elif not password:
            message = '管理员密码为必填项'
        if message:
            self.render('merchant-give-goldbean.html', username=username, message=message, customer_id=customer_id,
                        gb_num='', password='')
            return
        try:
            merchant.check_password(merchant_id, password)
            ref = merchant.give_goldbean(customer_id, gb_num)
        except Exception as e:
            self.render('merchant-give-goldbean.html', username=username, message=e.message, customer_id=customer_id,
                        gb_num='', password='')
            return
        if ref:
            self.render('merchant-give-goldbean.html', username=username, message='赠送成功', customer_id=customer_id,
                        gb_num='', password='')


class MerchantUpdatePasswordHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '2':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        self.render('merchant-update-password.html', username=username, message='')

    def post(self):
        merchant_id = self.get_secure_cookie('merchant_id')
        username = self.get_secure_cookie('username')
        old_password = self.get_argument('old_password')
        new_password1 = self.get_argument('new_password1')
        new_password2 = self.get_argument('new_password2')
        message = None
        if not old_password:
            message = '旧密码为必填项'
        elif not new_password1:
            message = '新密码为必填项'
        elif not new_password2:
            message = '请确认新密码'
        elif new_password1 != new_password2:
            message = '两次密码不一致'
        if message:
            self.render('merchant-give-goldbean.html', username=username, message=message)
            return
        try:
            merchant.check_password(merchant_id, old_password)
            ref = merchant.update_password(new_password1)
        except Exception as e:
            self.render('merchant-give-goldbean.html', username=username, message=e.message, customer_id=customer_id,
                        gb_num='', password='')
            return
        if ref:
            self.render('merchant-give-goldbean.html', username=username, message='赠送成功', customer_id=customer_id,
                        gb_num='', password='')
