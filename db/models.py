# -*- coding: utf-8 -*- 
"""
Created on 2015-9-1
@author: lsy
SQLAlchemy models for score data.
"""
import uuid
from sqlalchemy import Column, String, DateTime, Boolean, Float, Integer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import object_mapper
import datetime
from db.session import get_session

BASE = declarative_base()


def utc_now():
    """Overridable version of utils.utc_now."""
    if utc_now.override_time:
        try:
            return utc_now.override_time.pop(0)
        except AttributeError:
            return utc_now.override_time
    return datetime.datetime.now()

utc_now.override_time = None


class ScoreBase(object):
    """Base class for Score Models."""
    __table_args__ = {'mysql_engine': 'InnoDB'}
    __table_initialized__ = False
    id = Column(String(length=128), nullable=False, default=uuid.uuid1)
    created_at = Column(DateTime, default=utc_now())
    updated_at = Column(DateTime, onupdate=utc_now())
    deleted_at = Column(DateTime)
    deleted = Column(Boolean, default=False)
    metadata = None

    def __init__(self):
        self._i = None

    def save(self, session=None):
        """Save this object."""
        if not session:
            session = get_session()
        session.add(self)
        try:
            session.flush()
        except IntegrityError, e:
            if str(e).endswith('is not unique'):
                raise Exception.format(str(e))
            else:
                raise

    def delete(self, session=None):
        """Delete this object."""
        self.deleted = True
        self.deleted_at = utc_now()
        self.save(session=session)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def __iter__(self):
        self._i = iter(object_mapper(self).columns)
        return self

    def next(self):
        n = self._i.next().name
        return n, getattr(self, n)

    def update(self, values):
        """Make the model object behave like a dict."""
        for k, v in values.iteritems():
            setattr(self, k, v)

    def iteritems(self):
        """Make the model object behave like a dict.

        Includes attributes from joins."""
        local = dict(self)
        joined = dict([(k, v) for k, v in self.__dict__.iteritems()
                      if not k[0] == '_'])
        local.update(joined)
        return local.iteritems()

    def dict(self):
        item_list = []
        for k, v in self.__dict__.iteritems():
            if not k[0] == '_':
                if type(v) == datetime.datetime:
                    v = datetime.datetime.strftime(v, '%Y-%m-%d %H:%M:%S')
                item_list.append((k, v))

        joined = dict(item_list)
        return joined


# 用户表
class User(BASE, ScoreBase):
    """Represents a user
    """
    __tablename__ = 'user'
    id = Column(String(length=128), nullable=False, default=uuid.uuid1, primary_key=True)
    role = Column(String(length=255), nullable=False)
    username = Column(String(length=255), nullable=False)
    password = Column(String(length=255), nullable=False)


# 商家信息表
class Merchant(BASE, ScoreBase):
    """Represents a merchant
    """
    __tablename__ = 'merchant'
    id = Column(String(length=128), nullable=False, default=uuid.uuid1, primary_key=True)
    user_id = Column(String(128), nullable=False)
    name = Column(String(255), nullable=False)
    host_name = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    deadline = Column(DateTime(timezone=False), nullable=False)
    member_num = Column(Integer, nullable=False, default=0)
    gb_to_money = Column(Integer, nullable=False, default=0)
    gb_exchange_count = Column(Integer, nullable=False, default=0)


#  会员信息表
class Customer(BASE, ScoreBase):
    """Represents a customer
    """
    __tablename__ = 'customer'
    id = Column(String(length=128), nullable=False, default=uuid.uuid1, primary_key=True)
    user_id = Column(String(128), nullable=False)
    merchant_id = Column(String(128), nullable=True)
    serial_num = Column(Integer, nullable=False)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)
    identify_id = Column(String(255), nullable=True)
    we_chat = Column(String(255), nullable=True)
    gb = Column(Integer, nullable=False, default=0)
    total_gb = Column(Integer, nullable=False, default=0)
    given_gb = Column(Integer, nullable=False, default=0)
    consume_gb = Column(Integer, nullable=False, default=0)
    qualification_gb = Column(Integer, nullable=False, default=0)
    gb_exchange_count = Column(Integer, nullable=False, default=0)
    gain_money = Column(Integer, nullable=False, default=0)


#  会员信息表
class Goods(BASE, ScoreBase):
    """Represents a goods
    """
    __tablename__ = 'goods'
    id = Column(String(length=128), nullable=False, default=uuid.uuid1, primary_key=True)
    merchant_id = Column(String(128), nullable=False)
    serial_num = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    offer = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)
    sales_amount = Column(Integer, nullable=False, default=0)


#  积分兑换规则表
class Rule(BASE, ScoreBase):
    """Represents a rule,type为0代表积分,type为1代表人民币
    """
    __tablename__ = 'rule'
    id = Column(String(length=128), nullable=False, default=uuid.uuid1, primary_key=True)
    merchant_id = Column(String(128), nullable=False)
    level1 = Column(Integer, nullable=False)
    level2 = Column(Integer, nullable=False)
    level3 = Column(Integer, nullable=False)
    level4 = Column(Integer, nullable=False)
    level5 = Column(Integer, nullable=False)
    level6 = Column(Integer, nullable=False)
    level7 = Column(Integer, nullable=False)
    level8 = Column(Integer, nullable=False)
    rule_info = Column(String(128), nullable=False)


#  积分活动表
class Activity(BASE, ScoreBase):
    """Represents a activity
    """
    __tablename__ = 'activity'
    id = Column(String(length=128), nullable=False, default=uuid.uuid1, primary_key=True)
    merchant_id = Column(String(128), nullable=False)
    multiple = Column(Float, nullable=False)
    start_time = Column(DateTime(timezone=False))
    end_time = Column(DateTime(timezone=False))


#  消费表
class Consume(BASE, ScoreBase):
    """Represents a consume
    """
    __tablename__ = 'consume'
    id = Column(String(length=128), nullable=False, default=uuid.uuid1, primary_key=True)
    merchant_id = Column(String(128), nullable=False)
    goods_id = Column(String(128), nullable=False)
    customer_id = Column(String(128), nullable=True)
    consumer_name = Column(String(128), nullable=False)
    consumer_phone = Column(String(128), nullable=False)
    consume_money = Column(Integer, nullable=False)
    multiple = Column(Float, nullable=False)
    consume_content = Column(String(255), nullable=True)


#  兑换信息表
class Exchange(BASE, ScoreBase):
    """Represents a exchange
    """
    __tablename__ = 'exchange'
    id = Column(String(length=128), nullable=False, default=uuid.uuid1, primary_key=True)
    merchant_id = Column(String(128), nullable=False)
    customer_id = Column(String(128), nullable=False)
    customer_name = Column(String(128), nullable=False)
    exchange_money = Column(Integer, nullable=False)
    exchange_goldbean = Column(Integer, nullable=False)


if __name__ == '__main__':
    import time
    print time.strftime('%Y-%m-%d',time.localtime(time.time()+3600*24*2))
