#!/usr/bin/env Python
# coding=utf-8

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from orm.db_base import dbSession
from orm.db_base import DataBase

# 定义好一些属性，与user表中的字段进行映射，并且这个属性要属于某个类型


class UsersInfoModule(DataBase):

    __tablename__ = 'users_info'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(64), nullable=False, index=True)  # 用户名，工号
    chinese_name = Column(String(64), nullable=False, index=True)  # 中文名称
    nick_name = Column(String(64), nullable=False, index=True)  # 昵称
    pass_word = Column(String(64), nullable=False)  # 密码
    email = Column(String(64), nullable=False, index=True)  # 邮箱
    department = Column(String(64), nullable=False, index=True)  # 部门
    user_role = Column(String(64), nullable=False, index=True)  # 角色
    address = Column(String(128), nullable=False, index=True)  # 地址，备用
    pwd_modified = Column(Boolean, default=False, nullable=False)  # 密码是否修改
    change_pwd_count = Column(Integer, default=0, nullable=False, index=False)  # 密码修改次数

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.user_name)

    # 可以在类里面写别的方法,类似查询方法
    @classmethod
    def get_all_users_info(cls):
        return dbSession.query(cls).all()

    @classmethod
    def delete_user_by_name(cls, user_name):
        user_name = dbSession.query(cls).filter(cls.user_name == user_name).first()

        if user_name is not None:
            dbSession.delete(user_name)
            return True
        else:
            return False
