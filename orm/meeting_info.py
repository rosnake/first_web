#!/usr/bin/env Python
# coding=utf-8

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from orm.db_base import dbSession
from orm.db_base import DataBase
from datetime import datetime
# 定义好一些属性，与user表中的字段进行映射，并且这个属性要属于某个类型


class MeetingInfoModule(DataBase):
    """
    会议信息表
    """
    __tablename__ = 'meeting_info'

    id = Column(Integer, primary_key=True)
    keynote_user_name = Column(String(64), nullable=False, index=True)  # 主讲人用户名
    issues_id = Column(String(64), nullable=False, index=True)  # 议题ID
    keynote_chinese_name = Column(String(64), nullable=False, index=True)  # 主讲人中文名
    meeting_room = Column(String(64), nullable=False, index=True)  # 会议室
    issues_title = Column(String(64), nullable=False, index=True)  # 议题ID
    meeting_date = Column(DateTime, default=datetime.now())  # 会议时间
    current_meeting = Column(Boolean, default=True, nullable=False)  # 是否是当前会议
    meeting_finish = Column(Boolean, default=False, nullable=False)  # 会议是否结束

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.keynote_user_name)

    # 可以在类里面写别的方法,类似查询方法
    @classmethod
    def get_all_meeting_info(cls):
        return dbSession.query(cls).all()

