#!/usr/bin/env Python
# coding=utf-8

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from orm.db_base import dbSession
from orm.db_base import DataBase
from datetime import datetime
# 定义好一些属性，与user表中的字段进行映射，并且这个属性要属于某个类型


class FeedBackModule(DataBase):
    """
    议题信息表
    """
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True)
    serial_number = Column(String(64), nullable=False, index=True)  # 编号
    issues_title = Column(String(128), nullable=False)  # 问题名称
    issues_details = Column(String(256), nullable=True, index=False)  # 问题描述
    report_date = Column(DateTime, default=datetime.now())  # 报告日期
    resolved_date = Column(DateTime, default=datetime.now())  # 解决日期
    solution_methods = Column(String(256), nullable=True, index=False)  # 解决方案描述
    status = Column(String(64), nullable=False, index=True)  # 状态：open,closed,resolved etc.
    report_user_name = Column(String(64), nullable=False)  # 报告人
    resolved_user_name = Column(String(64), nullable=False)  # 解决人

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.serial_number)

    # 可以在类里面写别的方法,类似查询方法
    @classmethod
    def get_feedback_info(cls):
        return dbSession.query(cls).all()



