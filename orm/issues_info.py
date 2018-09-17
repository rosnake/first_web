#!/usr/bin/env Python
# coding=utf-8

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from orm.db_base import dbSession
from orm.db_base import DataBase
from datetime import datetime
# 定义好一些属性，与user表中的字段进行映射，并且这个属性要属于某个类型


class IssuesInfoModule(DataBase):
    """
    议题信息表
    """
    __tablename__ = 'issues_info'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(64), nullable=False, index=True)  # 用户名，工号
    chinese_name = Column(String(64), nullable=False, index=False)  # 中文名
    issues_title = Column(String(64), nullable=False)  # 议题名称
    issues_brief = Column(String(64), nullable=True, index=False)  # 议题简介
    issues_image = Column(String(64), nullable=True, index=False)  # 议题图片路径
    date_time = Column(DateTime, default=datetime.now())
    finish = Column(Boolean, default=False, nullable=False)
    current = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.user_name)

    # 可以在类里面写别的方法,类似查询方法
    @classmethod
    def get_all_issues_info(cls):
        return dbSession.query(cls).all()



