#!/usr/bin/env Python
# coding=utf-8

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from orm.db_base import dbSession
from orm.db_base import DataBase
from datetime import datetime
# 定义好一些属性，与user表中的字段进行映射，并且这个属性要属于某个类型


class ScoringCriteriaModule(DataBase):
    """
    积分规则
    """
    __tablename__ = 'scoring_criteria'

    id = Column(Integer, primary_key=True)
    criteria_name = Column(String(64), nullable=False, index=True)  # 分数项目名称
    score_value = Column(Float, default=0.0, nullable=False, index=False)  # 对应分数
    take_effect = Column(Boolean, default=True, nullable=False)  # 积分规则是否有效
    subtraction = Column(Boolean, default=True, nullable=False)  # 是否是扣分项目

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.criteria_name)

    # 可以在类里面写别的方法,类似查询方法
    @classmethod
    def get_all_scoring_criteria(cls):
        return dbSession.query(cls).all()



