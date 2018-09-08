#!/usr/bin/env Python
# coding=utf-8

# 连接数据库的数据

HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = 'web_db'
USERNAME = 'root'
PASSWORD = 'tornado123'

# DB_URI的格式：dialect（mysql/sqlite）+driver://username:password@host:port/database?charset=utf8

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
