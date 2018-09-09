#!/usr/bin/env Python
# coding=utf-8

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from orm.db import dbSession
from orm.db import DataBase

# 定义好一些属性，与user表中的字段进行映射，并且这个属性要属于某个类型


class UserModule(DataBase):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, index=True)  # 用户名，工号
    nickname = Column(String(64), nullable=False, index=True)  # 中文名称
    password = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False, index=True)  # 邮箱
    department = Column(String(64), nullable=False, index=True)  # 部门
    role = Column(String(64), nullable=False, index=True)  # 角色
    address = Column(String(128), nullable=False, index=True)  # 地址，备用
    pwd_modified = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.username)

    # 可以在类里面写别的方法,类似查询方法
    @classmethod
    def get_all_users(cls):
        return dbSession.query(cls).all()

    @classmethod
    def delete_user_by_name(cls, username):
        username = dbSession.query(cls).filter(cls.username == username).first()

        if username is not None:
            dbSession.delete(username)
            return True
        else:
            return False
