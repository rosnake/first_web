#!/usr/bin/env Python
# coding=utf-8

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from orm.db import dbSession
from orm.db import DataBase
from datetime import datetime
# 定义好一些属性，与attendance表中的字段进行映射，并且这个属性要属于某个类型


class AttendanceModule(DataBase):

    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, index=True)  # 用户名
    nickname = Column(String(64), nullable=True, index=False)  # 昵称，即中文名
    absence_reason = Column(String(64), nullable=True, index=False)  # 缺席原因
    absence_id = Column(Integer, nullable=False)
    attend = Column(Boolean, default=True, nullable=False, index=False)  # 是否出席
    absent_accept = Column(Boolean, default=False, nullable=False, index=False)  # 是否出席
    apply_time = Column(DateTime, default=datetime.now())  # 申请时间
    datetime = Column(DateTime, default=datetime.now())  # 申请时间

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.username)

    # 可以在类里面写别的方法,类似查询方法
    @classmethod
    def get_all_attendance_info(cls):
        return dbSession.query(cls).all()
