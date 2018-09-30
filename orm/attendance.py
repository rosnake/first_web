#!/usr/bin/env Python
# coding=utf-8

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from orm.db_base import dbSession
from orm.db_base import DataBase
from datetime import datetime
# 定义好一些属性，与attendance表中的字段进行映射，并且这个属性要属于某个类型
# 人员出勤表


class AttendanceModule(DataBase):
    """
    出勤签到表
    """
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(64), nullable=False, index=True)  # 用户名
    chinese_name = Column(String(64), nullable=True, index=False)  # 昵称，即中文名
    absence_reason = Column(String(64), nullable=True, index=False)  # 缺席原因
    absence_id = Column(Integer, nullable=False)  # 缺席原因对于的ID
    attended = Column(Boolean, default=True, nullable=False, index=False)  # 是否出席，True表示出席，FALSE表示未出席
    checked_in = Column(Boolean, default=False, nullable=False, index=False)  # 是否已签到
    absence_apply_accept = Column(Boolean, default=False, nullable=False, index=False)  # 请假申请是否接受
    absence_apply_time = Column(DateTime, default=datetime.now())  # 缺席申请时间
    meeting_date_time = Column(DateTime, default=datetime.now())  # 会议时间
    current_attendance = Column(Boolean, default=False, nullable=False, index=False)  # 当前签到表
    date_time = Column(DateTime, default=datetime.now())  # 当前时间

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.user_name)

    # 可以在类里面写别的方法,类似查询方法
    @classmethod
    def get_all_attendance_info(cls):
        return dbSession.query(cls).all()
