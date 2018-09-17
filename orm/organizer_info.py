#!/usr/bin/env Python
# coding=utf-8

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from orm.db_base import dbSession
from orm.db_base import DataBase
from datetime import datetime


# 定义好一些属性，与user表中的字段进行映射，并且这个属性要属于某个类型


class OrganizerInfoModule(DataBase):
    """
    组织者信息表
    """
    __tablename__ = 'organizer_info'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(64), nullable=False, index=True)  # 组织者用户名
    chinese_name = Column(String(64), nullable=False, index=True)  # 组织者中文名
    current = Column(Boolean, default=False, nullable=False)  # 是否是当前组织者
    date_time = Column(DateTime, default=datetime.now())  # 组织时间

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.user_name)

    # 可以在类里面写别的方法,类似查询方法
    @classmethod
    def get_all_organizer_info(cls):
        return dbSession.query(cls).all()



