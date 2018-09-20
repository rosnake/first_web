#!/usr/bin/env Python
# coding=utf-8

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from orm.db_base import dbSession
from orm.db_base import DataBase

# 定义好一些属性，与user表中的字段进行映射，并且这个属性要属于某个类型


class ScoreInfoModule(DataBase):
    """
    积分信息表
    """
    __tablename__ = 'score_info'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(64), nullable=False, index=True)  # 用户名，工号
    chinese_name = Column(String(64), nullable=False, index=True)  # 用户名，中文名
    current_scores = Column(Float, default=0.0, nullable=False, index=False)  # 当前积分
    last_scores = Column(Float, default=0.0, nullable=False, index=False)   # 上周积分

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.user_name)

    # 可以在类里面写别的方法,类似查询方法
    @classmethod
    def get_all_score_info(cls):
        return dbSession.query(cls).all()



