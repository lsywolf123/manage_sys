# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy


class ScoreException(Exception):
    code = 0
    message = "Score Exception Default"
    format_msg = ""

    def __init__(self, code=0, message=None):
        self.code = code
        if message:
            self.message = message

    def format(self, *args):
        self.message = self.format_msg % args
        return self


class UserIsNotExistException(ScoreException):
    code = 10001
    message = '用户名不存在!'


class UserIsExistException(ScoreException):
    code = 10002
    message = '用户名已存在!'


class PasswordIsWrongException(ScoreException):
    code = 10003
    message = '密码错误 !'


class PhoneIsExistException(ScoreException):
    code = 10004
    message = '手机号码已存在!'


class SerialNumIsAlreadyBinded(ScoreException):
    code = 10005
    message = '该编号已经被绑定!'


class SerialNumIsNotExist(ScoreException):
    code = 10006
    message = '该编号不存在!'


class CustomerInfoNotMatch(ScoreException):
    code = 10007
    message = '会员信息不匹配!'


class CustomerGoldbeanNotEnough(ScoreException):
    code = 10007
    message = '会员积分不足兑换该档次!'


class CustomerHasNoQualification(ScoreException):
    code = 10008
    message = '会员的推荐基金没达到5000,没有兑换资格'


class GoodsIsExistException(ScoreException):
    code = 10009
    message = '商品已存在!'


class GoodsIsNotExistException(ScoreException):
    code = 10010
    message = '商品不存在!'


class GoodsIsNotEnoughException(ScoreException):
    code = 10011
    message = '商品库存不足,无法创建消费订单!'


class SerialNumIsNotBind(ScoreException):
    code = 10012
    message = '无法查到该推荐人编号所对应的推荐人!'