#!/usr/bin/env Python
# coding=utf-8

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from orm.db_base import dbSession
from orm.db_base import DataBase
from datetime import datetime
# 定义好一些属性，与user表中的字段进行映射，并且这个属性要属于某个类型


class ExchangeRulesModule(DataBase):
    """
    积分兑换规则表
    """
    __tablename__ = 'exchange_rules'

    id = Column(Integer, primary_key=True)
    exchange_rule_name = Column(String(64), nullable=False, index=True)  # 分数项目名称
    exchange_rule_score = Column(Float, default=0.0, nullable=False, index=False)  # 对应分数
    exchange_min_score = Column(Float, default=0.0, nullable=False, index=False)  # 最少分数

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.exchange_rule_name)

    # 可以在类里面写别的方法,类似查询方法
    @classmethod
    def get_all_exchange_rules(cls):
        return dbSession.query(cls).all()



