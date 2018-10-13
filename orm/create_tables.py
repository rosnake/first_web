#!/usr/bin/env Python
# coding=utf-8

from orm.db_base import dbSession
from orm.db_base import engine
from orm.db_base import DataBase
from orm.users_info import UsersInfoModule
from config.default_user import DefaultAdminUser
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


# 将创建好的数据表类，映射到数据库的表中


def create_all_tables():
    print('------------create_all-------------')
    DataBase.metadata.create_all(engine)
    print('------------create_end-------------')


def create_root_user():
    # 先查询用户是否存在
    user = dbSession.query(UsersInfoModule).filter(UsersInfoModule.user_name == "root").first()
    # 不存在创建用户
    if user is None:
        user_module = UsersInfoModule()
        user_module.user_name = DefaultAdminUser.user_name
        user_module.chinese_name = DefaultAdminUser.chinese_name
        user_module.nick_name = DefaultAdminUser.nick_name
        user_module.pass_word = DefaultAdminUser.pass_word
        user_module.address = DefaultAdminUser.address
        user_module.department = DefaultAdminUser.department
        user_module.email = DefaultAdminUser.email
        user_module.user_role = DefaultAdminUser.user_role
        user_module.pwd_modified = False
        user_module.change_pwd_count = 0

        dbSession.add(user_module)
        dbSession.commit()
