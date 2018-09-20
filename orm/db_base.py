#!/usr/bin/env Python
# coding=utf-8

from config.db_settings import *
# 引入基本的包
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


#  from methods.debug import *

# 创建引擎

engine = create_engine(DB_URI, echo=False)
# session maker生成一个session类
Session = sessionmaker(bind=engine)
dbSession = Session()

DataBase = declarative_base(engine)
