#!/usr/bin/env Python
# coding=utf-8

import datetime

class DateToolKits:
    def __init__(self):
        self.now_day_str = "1970-01-01"
        self.now_second_str = "1970-01-01 11:59:58"
        self.now_time = datetime.datetime.now()

    def get_now_day_str(self):
        now_time = datetime.datetime.now()
        self.now_day_str = now_time.strftime('%Y-%m-%d')
        return self.now_day_str

    def get_now_second_str(self):
        now_time = datetime.datetime.now()
        self.now_second_str = now_time.strftime('%Y-%m-%d %H:%M:%S')  # 现在
        return self.now_second_str

    def get_now_time(self):
        self.now_time = datetime.datetime.now()
        return self.now_time


