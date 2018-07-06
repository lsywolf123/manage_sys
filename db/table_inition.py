# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, Float


engine = create_engine('mysql://root:123456@127.0.0.1:3306/jindou_system?charset=utf8', echo=False)
metadata = MetaData(engine)
table_list = []

# 创建数据库表
user_table = Table('user', metadata,
                   Column('id', String(128), primary_key=True),
                   Column('role', String(255), nullable=False),
                   Column('username', String(255), nullable=False),
                   Column('password', String(255), nullable=False),
                   Column('created_at', DateTime(timezone=False)),
                   Column('updated_at', DateTime(timezone=False)),
                   Column('deleted_at', DateTime(timezone=False)),
                   Column('deleted', Boolean(create_constraint=True, name=None))
                   )
table_list.append(user_table)


merchant_table = Table('merchant', metadata,
                       Column('id', String(128), primary_key=True),
                       Column('user_id', String(128), nullable=False),
                       Column('name', String(255), nullable=False),
                       Column('host_name', String(255), nullable=False),
                       Column('phone', String(255), nullable=False),
                       Column('email', String(255), nullable=False),
                       Column('address', String(255), nullable=False),
                       Column('deadline', DateTime(timezone=False), nullable=False),
                       Column('member_num', Integer, nullable=False),
                       Column('gb_to_money', Integer, nullable=False),
                       Column('gb_exchange_count', Integer, nullable=False),
                       Column('created_at', DateTime(timezone=False)),
                       Column('updated_at', DateTime(timezone=False)),
                       Column('deleted_at', DateTime(timezone=False)),
                       Column('deleted', Boolean(create_constraint=True, name=None))
                       )
table_list.append(merchant_table)


customer_table = Table('customer', metadata,
                       Column('id', String(128), primary_key=True),
                       Column('user_id', String(128), nullable=False),
                       Column('merchant_id', String(128), nullable=True),
                       Column('serial_num', Integer, nullable=False),
                       Column('name', String(255), nullable=True),
                       Column('email', String(255), nullable=True),
                       Column('phone', String(255), nullable=True),
                       Column('identify_id', String(255), nullable=True),
                       Column('we_chat', String(255), nullable=True),
                       Column('gb', Integer, nullable=False),
                       Column('total_gb', Integer, nullable=False),
                       Column('given_gb', Integer, nullable=False),
                       Column('consume_gb', Integer, nullable=False),
                       Column('qualification_gb', Integer, nullable=False),
                       Column('gb_exchange_count', Integer, nullable=False),
                       Column('gain_money', Integer, nullable=False),
                       Column('created_at', DateTime(timezone=False)),
                       Column('updated_at', DateTime(timezone=False)),
                       Column('deleted_at', DateTime(timezone=False)),
                       Column('deleted', Boolean(create_constraint=True, name=None))
                       )
table_list.append(customer_table)


rule_table = Table('rule', metadata,
                   Column('id', String(128), primary_key=True),
                   Column('merchant_id', String(128), primary_key=True),
                   Column('level1', Integer, nullable=False),
                   Column('level2', Integer, nullable=False),
                   Column('level3', Integer, nullable=False),
                   Column('level4', Integer, nullable=False),
                   Column('level5', Integer, nullable=False),
                   Column('level6', Integer, nullable=False),
                   Column('level7', Integer, nullable=False),
                   Column('level8', Integer, nullable=False),
                   Column('rule_info',  String(128), nullable=False),
                   Column('created_at', DateTime(timezone=False)),
                   Column('updated_at', DateTime(timezone=False)),
                   Column('deleted_at', DateTime(timezone=False)),
                   Column('deleted', Boolean(create_constraint=True, name=None))
                   )
table_list.append(rule_table)


activity_table = Table('activity', metadata,
                       Column('id', String(128), primary_key=True),
                       Column('merchant_id', String(128), nullable=False),
                       Column('multiple', Float, nullable=False),
                       Column('start_time', DateTime(timezone=False)),
                       Column('end_time', DateTime(timezone=False)),
                       Column('created_at', DateTime(timezone=False)),
                       Column('updated_at', DateTime(timezone=False)),
                       Column('deleted_at', DateTime(timezone=False)),
                       Column('deleted', Boolean(create_constraint=True, name=None))
                       )
table_list.append(activity_table)


consume_table = Table('consume', metadata,
                      Column('id', String(128), primary_key=True),
                      Column('merchant_id', String(128), nullable=False),
                      Column('goods_id', String(128), nullable=False),
                      Column('customer_id', String(128), nullable=True),
                      Column('consumer_name', String(128), nullable=False),
                      Column('consumer_phone', String(128), nullable=False),
                      Column('consume_money', Integer, nullable=False),
                      Column('multiple', Float, nullable=False),
                      Column('consume_content', String(255), nullable=True),
                      Column('created_at', DateTime(timezone=False)),
                      Column('updated_at', DateTime(timezone=False)),
                      Column('deleted_at', DateTime(timezone=False)),
                      Column('deleted', Boolean(create_constraint=True, name=None))
                      )
table_list.append(consume_table)


exchange_table = Table('exchange', metadata,
                       Column('id', String(128), primary_key=True),
                       Column('merchant_id', String(128), nullable=False),
                       Column('customer_id', String(128), nullable=False),
                       Column('customer_name', String(128), nullable=False),
                       Column('exchange_money', Integer, nullable=False),
                       Column('exchange_goldbean', Integer, nullable=False),
                       Column('created_at', DateTime(timezone=False)),
                       Column('updated_at', DateTime(timezone=False)),
                       Column('deleted_at', DateTime(timezone=False)),
                       Column('deleted', Boolean(create_constraint=True, name=None)))
table_list.append(exchange_table)


goods_table = Table('goods', metadata,
                       Column('id', String(128), primary_key=True),
                       Column('merchant_id',String(128), nullable=True),
                       Column('serial_num',String(255), nullable=False),
                       Column('name', String(255), nullable=True),
                       Column('price', Integer, nullable=True),
                       Column('offer', Integer, nullable=True),
                       Column('stock', Integer, nullable=True),
                       Column('sales_amount', Integer, nullable=True),
                       Column('created_at', DateTime(timezone=False)),
                       Column('updated_at', DateTime(timezone=False)),
                       Column('deleted_at', DateTime(timezone=False)),
                       Column('deleted', Boolean(create_constraint=True, name=None)))
table_list.append(goods_table)

#  删除所有表
# for table in table_list:
#     try:
#         table.drop()
#         print "Drop Table %s Success !"%table.fullname
#     except Exception,e:
#         print e.message


# 创建所有表
for table in table_list:
    try:
        table.create()
        print "Create Table %s Success !"%table.fullname
    except Exception,e:
        print e.message


# 创建单个表
# application_table.create()