#!/usr/bin/env Python
# coding=utf-8

# 连接数据库的数据
from methods.debug import *
import pymysql
from config.db_settings import DbSetting
from orm.score_info import ScoreInfoModule
from orm.exchange_apply import ExchangeApplyModule
from orm.organizer_info import OrganizerInfoModule
from orm.issues_info import IssuesInfoModule
from orm.score_criteria import ScoringCriteriaModule
from orm.exchange_rules import ExchangeRulesModule
from orm.attendance import AttendanceModule
from orm.score_history import ScoringHistoryModule
from orm.meeting_info import MeetingInfoModule
from orm.evaluation_info import EvaluationInfoModule
from orm.operation_history import OperationHistoryModule
from orm.users_info import UsersInfoModule
from orm.exchanged_history import ExchangedHistoryModule
from config.debug import DebugConfig
from orm.assessment import AssessmentInfoModule
def drop_db_table():
    port = int(DbSetting.listen_port)
    connect = pymysql.connect(  # 连接数据库服务器
        user=DbSetting.user_name,
        password=DbSetting.pass_word,
        host=DbSetting.host_name,
        port=port,
        db=DbSetting.database_name,
        charset="utf8"
    )
    conn_cursor = connect.cursor()  # 创建操作游标
    # 你需要一个游标 来实现对数据库的操作相当于一条线索
    sql = "drop table if exists " + ScoreInfoModule.__tablename__
    logging.info("execute: "+sql)
    conn_cursor.execute(sql)  # 如果表存在则删除

    sql = "drop table if exists " + ExchangeApplyModule.__tablename__
    logging.info("execute: "+sql)
    conn_cursor.execute(sql)  # 如果表存在则删除

    sql = "drop table if exists " + OrganizerInfoModule.__tablename__
    logging.info("execute: "+sql)
    conn_cursor.execute(sql)  # 如果表存在则删除

    sql = "drop table if exists " + IssuesInfoModule.__tablename__
    logging.info("execute: "+sql)
    conn_cursor.execute(sql)  # 如果表存在则删除

    sql = "drop table if exists " + AttendanceModule.__tablename__
    logging.info("execute: "+sql)
    conn_cursor.execute(sql)  # 如果表存在则删除

    sql = "drop table if exists " + ScoringHistoryModule.__tablename__
    logging.info("execute: "+sql)
    conn_cursor.execute(sql)  # 如果表存在则删除

    sql = "drop table if exists " + MeetingInfoModule.__tablename__
    logging.info("execute: "+sql)
    conn_cursor.execute(sql)  # 如果表存在则删除

    sql = "drop table if exists " + EvaluationInfoModule.__tablename__
    logging.info("execute: "+sql)
    conn_cursor.execute(sql)  # 如果表存在则删除

    sql = "drop table if exists " + OperationHistoryModule.__tablename__
    logging.info("execute: "+sql)
    conn_cursor.execute(sql)  # 如果表存在则删除

    sql = "drop table if exists " + UsersInfoModule.__tablename__
    logging.info("execute: "+sql)
    conn_cursor.execute(sql)  # 如果表存在则删除

    sql = "drop table if exists " + ExchangedHistoryModule.__tablename__
    logging.info("execute: "+sql)
    conn_cursor.execute(sql)  # 如果表存在则删除

    sql = "drop table if exists " + AssessmentInfoModule.__tablename__
    logging.info("execute: "+sql)
    conn_cursor.execute(sql)  # 如果表存在则删除

    if DebugConfig.DEBUG is not True:

        sql = "drop table if exists " + ScoringCriteriaModule.__tablename__
        logging.info("execute: "+sql)
        conn_cursor.execute(sql)  # 如果表存在则删除

        sql = "drop table if exists " + ExchangeRulesModule.__tablename__
        logging.info("execute: "+sql)
        conn_cursor.execute(sql)  # 如果表存在则删除

    conn_cursor.close()  # 关闭游标连接
    connect.close()  # 关闭数据库服务器连接 释放内存

