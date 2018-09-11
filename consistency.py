#!/usr/bin/env Python
# coding=utf-8

import time, threading
from methods.debug import *
from orm.db import dbSession
from orm.attendance import AttendanceModule
from orm.user import UserModule
from multiprocessing import Process
import os


# 数据库资源一致性线程
class DataConsistency:

    def __init__(self):
        logging.info("call data consistency init ")
        self.db = dbSession

    def processing(self):
        logging.info("start data consistency processing")

        self.__process_attendance_table()
        logging.info("finish data consistency processing")

    def run(self):
        logging.info("run data consistency processing")
        thread = threading.Thread(target=self.processing(), name='ProcessingThread')
        thread.start()
        thread.join()
        self.db.close()

    def __process_attendance_table(self):
        attendance_modules = AttendanceModule.get_all_attendance_info()
        user_modules = UserModule.get_all_users()
        if attendance_modules:
            pass
        else:
            for x in user_modules:
                attendance = AttendanceModule()
                attendance.username = x.username
                attendance.nickname = x.nickname
                attendance.absence_id = 0
                attendance.attend = True
                attendance.absence_id = 0
                self.db.add(attendance)
                self.db.commit()


