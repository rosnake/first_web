#!/usr/bin/env Python
# coding=utf-8

from orm.db import engine
from orm.db import DataBase

from orm.user import UserModule
from orm.points import PointsModule
from orm.exchange import ExchangeModule
from orm.organizer import OrganizerModule
from orm.topics import TopicsModule
from orm.marks import MarksModule
from orm.rules import ExchangeRuleModule
from orm.attendance import AttendanceModule
from orm.history import HistoryModule
from orm.meeting import MeetingModule


# 将创建好的数据表类，映射到数据库的表中


def create_all_tables():
    print('------------create_all-------------')
    DataBase.metadata.create_all(engine)
    print('------------create_end-------------')
