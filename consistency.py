#!/usr/bin/env Python
# coding=utf-8

import time, threading
from methods.debug import *
from orm.db_base import dbSession
from orm.attendance import AttendanceModule
from orm.users_info import UsersInfoModule
from orm.score_info import ScoreInfoModule
from config.default_config import DefaultScoreConfig
import os


# 数据库资源一致性线程
class DataConsistency:

    def __init__(self):
        logging.info("call data consistency init ")
        self.db = dbSession

    def processing(self):
        logging.info("start data consistency processing")

        self.__process_attendance_table()
        self.__process_score_table()
        logging.info("finish data consistency processing")

    def run(self):
        logging.info("run data consistency processing")
        thread = threading.Thread(target=self.processing(), name='ProcessingThread')
        thread.start()
        thread.join()
        self.db.close()

    def __process_attendance_table(self):
        attendance_modules = AttendanceModule.get_all_attendance_info()
        user_modules = UsersInfoModule.get_all_users_info()
        if attendance_modules:
            pass
        else:
            for x in user_modules:
                attendance = AttendanceModule()
                attendance.user_name = x.user_name
                attendance.chinese_name = x.chinese_name
                attendance.absence_id = 0
                attendance.attended = True
                attendance.absence_id = 0
                self.db.add(attendance)
                self.db.commit()

    def __process_score_table(self):
        score_modules = ScoreInfoModule.get_all_score_info()
        user_modules = UsersInfoModule.get_all_users_info()
        if score_modules:
            pass
        else:
            for x in user_modules:
                point_module = ScoreInfoModule()
                point_module.user_name = x.user_name
                point_module.current_scores = DefaultScoreConfig.current_scores
                point_module.last_scores = DefaultScoreConfig.last_scores
                point_module.chinese_name = x.chinese_name
                point_module.purchase_points = False
                self.db.add(point_module)
                self.db.commit()
