#!/usr/bin/env Python
# coding=utf-8

from orm.db import engine
from orm.user import Base


#将创建好的User类，映射到数据库的users表中

def run():
    print('------------create_all-------------')
    Base.metadata.create_all(engine)
    print('------------create_end-------------')