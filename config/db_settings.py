#!/usr/bin/env Python
# coding=utf-8

# 连接数据库的数据

HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = 'web_db'
user_name = 'root'
PASSWORD = 'tornado123'

# DB_URI的格式：dialect（mysql/sqlite）+driver://user_name:password@host:port/database?charset=utf8

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(user_name, PASSWORD, HOSTNAME, PORT, DATABASE)
