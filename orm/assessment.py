#!/usr/bin/env Python
# coding=utf-8

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from orm.db_base import DataBase
from datetime import datetime
# 定义好一些属性，与user表中的字段进行映射，并且这个属性要属于某个类型


class AssessmentInfoModule(DataBase):
    """
    议题兴趣评估表
    """
    __tablename__ = 'assessment_info'

    id = Column(Integer, primary_key=True)
    issues_id = Column(Integer, nullable=False, index=True)   # 议题ID
    assessment_user_name = Column(String(64), nullable=False, index=True)  # 评估者用户名
    assessment_time = Column(DateTime, default=datetime.now())  # 评估时间

    assessment_finish = Column(Boolean, default=False, nullable=False)  # 是否结束评估
    uninterested = Column(Boolean, default=False, nullable=False)  # 不感兴趣
    interested = Column(Boolean, default=False, nullable=False)  # 感兴趣

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.assessment_user_name)




