#!/usr/bin/env Python
# coding=utf-8

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from orm.db_base import DataBase
from datetime import datetime
# 定义好一些属性，与user表中的字段进行映射，并且这个属性要属于某个类型


class EvaluationInfoModule(DataBase):
    """
    积分评价表
    """
    __tablename__ = 'evaluation_info'

    id = Column(Integer, primary_key=True)
    issues_id = Column(String(64), nullable=False, index=True)   # 议题ID
    issues_title = Column(String(64), nullable=False, index=False)  # 议题名称
    keynote_user_name = Column(String(64), nullable=False, index=True)  # 主讲人用户名
    evaluate_user_name = Column(String(64), nullable=False, index=True)  # 评价者用户名
    evaluate_time = Column(DateTime, default=datetime.now())  # 评价时间

    issues_prepare_score = Column(Float, default=0.0, nullable=False, index=False)  # 议题准备情况得分
    issues_content_score = Column(Float, default=0.0, nullable=False, index=False)  # 议题内容得分
    issues_lecture_score = Column(Float, default=0.0, nullable=False, index=False)  # 演讲情况得分
    issues_reserved_score = Column(Float, default=0.0, nullable=False, index=False)  # 保留备用
    evaluate_finish = Column(Boolean, default=False, nullable=False)  # 是否结束评价
    date_time = Column(DateTime, default=datetime.now())  # 结束时间

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.evaluate_time)




