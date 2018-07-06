# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
import os
import tornado.ioloop
import tornado.web
from handle import test
from handle import login
from handle import index
from handle import manager
from handle import logout
from handle import merchant
from handle import customer
from handle import update_password
from handle import goods


ROOT = os.path.dirname(__file__)
STATIC_PATH = os.path.join(ROOT, "templates")
TMP_PATH = os.path.join(ROOT, "templates")

settings = {
    'template_path': TMP_PATH,
    "static_path": STATIC_PATH,
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o",
    "login_url": "/login",
}

application = tornado.web.Application(
    [
        (r"/test", test.IndexHandle),
        (r"/index", index.IndexHandle),
        (r'/login', login.LoginHandle),
        (r'/logout', logout.LogoutHandle),
        (r'/update-password', update_password.UpdatePasswordHandle),
        (r'/add-merchant', manager.AddMerchantHandle),
        (r'/manager-merchant-list', manager.MerchantListHandle),
        (r'/manager-customer-list', manager.CustomerListHandle),
        (r'/manager-update-merchant', manager.UpdateMerchantHandle),
        (r'/manager-delete-merchant', manager.DeleteMerchantHandle),
        (r'/manager-customer-info', manager.ManagerCustomerInfoHandle),
        (r'/add-customer', manager.AddCustomerHandle),
        (r'/add-customer-list', manager.CustomerAddedListHandle),
        (r'/add-customer-info', manager.CustomerAddedInfoHandle),
        (r'/merchant-bind-customer', merchant.MerchantBindCustomerHandle),
        (r'/merchant-customer-list', merchant.MerchantCustomerListHandle),
        (r'/merchant-customer-info', merchant.MerchantCustomerInfoHandle),
        (r'/merchant-customer-consumpt', merchant.MerchantCustomerConsumptHandle),
        (r'/merchant-rule', merchant.MerchantRuleHandle),
        (r'/merchant-update-rule', merchant.MerchantUpdateRuleHandle),
        (r'/merchant-update-rule-info', merchant.MerchantUpdateRuleInfoHandle),
        (r'/merchant-goldbean', merchant.MerchantGoldbeanHandle),
        (r'/merchant-update-goldbean', merchant.MerchantUpdateGoldbeanHandle),
        (r'/merchant-exchange-goldbean', merchant.MerchantExchangeGoldbeanHandle),
        (r'/merchant-consume-list', merchant.MerchantConsumeListHandle),
        (r'/merchant-consume-info', merchant.MerchantConsumeInfoHandle),
        (r'/merchant-exchange-list', merchant.MerchantExchangeListHandle),
        (r'/merchant-give-goldbean', merchant.MerchantGiveGbHandle),
        (r'/customer-goldbean-info', customer.CustomerGbInfoHandle),
        (r'/customer-goldbean-activity', customer.CustomerGbActivityHandle),
        (r'/customer-info', customer.CustomerInfoHandle),
        (r'/customer-info-update', customer.CustomerInfoUpdateHandle),
        (r'/merchant-add-goods', goods.AddGoodsHandle),
        (r'/merchant-goods-list', goods.GoodsListHandle),
        (r'/merchant-update-goods', goods.UpdategoodsHandle),
        (r'/merchant-delete-goods', goods.DeleteGoodsHandle),
        (r'/merchant-account-book', merchant.MerchantAccountBookHandle),
        (r'/merchant-account-analysis', merchant.MerchantAccountAnalysisHandle)
    ], **settings)


if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    print 'server 0.0.0.0:8000 started'