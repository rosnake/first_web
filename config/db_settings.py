#!/usr/bin/env Python
# coding=utf-8

# 连接数据库的数据


class DbSetting:

    host_name = 'localhost'
    listen_port = '3306'
    database_name = 'web_db'
    user_name = 'root'
    pass_word = 'tornado123'

# DB_URI的格式：dialect（mysql/sqlite）+driver://user_name:password@host:port/database?charset=utf8


DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(DbSetting.user_name, DbSetting.pass_word,
                                                              DbSetting.host_name, DbSetting.listen_port,
                                                              DbSetting.database_name)
