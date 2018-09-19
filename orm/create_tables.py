#!/usr/bin/env Python
# coding=utf-8

from orm.db_base import dbSession
from orm.db_base import engine
from orm.db_base import DataBase
from orm.users_info import UsersInfoModule
from orm.score_info import ScoreInfoModule
from orm.exchange_apply import ExchangeApplyModule
from orm.organizer_info import OrganizerInfoModule
from orm.issues_info import IssuesInfoModule
from orm.score_criteria import ScoringCriteriaModule
from orm.exchange_rules import ExchangeRulesModule
from orm.attendance import AttendanceModule
from orm.score_history import ScoringHistoryModule
from orm.meeting_info import MeetingInfoModule


# 将创建好的数据表类，映射到数据库的表中


def create_all_tables():
    print('------------create_all-------------')
    DataBase.metadata.create_all(engine)
    print('------------create_end-------------')


def create_root_user():
    # 先查询用户是否存在
    user = dbSession.query(UsersInfoModule).filter(UsersInfoModule.user_name == "admin").first()
    # 不存在创建用户
    if user is None:
        user_moudle = UsersInfoModule()
        user_moudle.user_name = "admin"
        user_moudle.chinese_name = "根用户"
        user_moudle.pass_word = "admin123"
        user_moudle.chinese_name = "unknown"
        user_moudle.address = "unknown"
        user_moudle.department = "unknown"
        user_moudle.email = "unknown"
        user_moudle.user_role = "admin"
        user_moudle.pwd_modified = False
        user_moudle.change_pwd_count = 0

        dbSession.add(user_moudle)
        dbSession.commit()
