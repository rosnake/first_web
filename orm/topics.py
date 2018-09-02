#!/usr/bin/env Python
# coding=utf-8

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from orm.db import dbSession
from orm.db import DataBase
from datetime import datetime
# 定义好一些属性，与user表中的字段进行映射，并且这个属性要属于某个类型


class TopicsModule(DataBase):

    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, index=True)  # 用户名，工号
    nickname = Column(String(64), nullable=False, index=False)  # 中文名
    title = Column(String(64), nullable=False)  # 议题名称
    brief = Column(String(64), nullable=True, index=False)  # 议题简介
    image = Column(String(64), nullable=True, index=False)  # 议题图片路径
    datetime = Column(DateTime, default=datetime.now())
    finish = Column(Boolean, default=False, nullable=False)
    current = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.username)

    # 可以在类里面写别的方法,类似查询方法
    @classmethod
    def get_all_topics(cls):
        return dbSession.query(cls).all()



