#!/usr/bin/env Python
# coding=utf-8

from sqlalchemy import Column, Integer, String, DateTime
from orm.db_base import DataBase
from datetime import datetime
# 定义好一些属性，与user表中的字段进行映射，并且这个属性要属于某个类型


class OperationHistoryModule(DataBase):
    """
    操作历史消息
    """
    __tablename__ = 'operation_history'

    id = Column(Integer, primary_key=True)
    operation_user_name = Column(String(64), nullable=False, index=True)  # 操作者用户名
    operation_details = Column(String(256), nullable=False, index=False)  # 操作详情
    operation_time = Column(DateTime, default=datetime.now())  # 申请时间

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.operation_user_name)





