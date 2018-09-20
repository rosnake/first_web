#!/usr/bin/env Python
# coding=utf-8

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from orm.db_base import dbSession
from orm.db_base import DataBase
from datetime import datetime
# 定义好一些属性，与user表中的字段进行映射，并且这个属性要属于某个类型


class ExchangeApplyModule(DataBase):
    """
    积分兑换申请表
    """
    __tablename__ = 'exchange_apply'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(64), nullable=False, index=True)  # 分数项目名称
    current_scores = Column(Float, default=0.0, nullable=False, index=False)  # 当前分数
    exchange_item = Column(String(64), nullable=False, index=True)  # 兑换项目名称
    need_score = Column(Float, default=0.0, nullable=False, index=False)  # 需要分数
    exchange_accept = Column(Boolean, default=False, nullable=False)  # 兑换申请是否已经被接受
    exchange_status = Column(String(64), nullable=False, index=True)  # 兑换项目名称
    date_time = Column(DateTime, default=datetime.now())  # 申请时间

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.user_name)

    # 可以在类里面写别的方法,类似查询方法
    @classmethod
    def get_all_exchange_apply_info(cls):
        return dbSession.query(cls).all()



