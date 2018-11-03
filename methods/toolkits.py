#!/usr/bin/env Python
# coding=utf-8

import datetime
import time
from methods.debug import *

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

    def get_now_str(self):
        now_time = datetime.datetime.now()
        self.now_second_str = now_time.strftime('%Y%m%d%H%M%S')  # 现在
        return self.now_second_str

    def cac_time_diff_by_str(self, string_time_src, string_time_dst):
        # 字符串变成时间数据结构
        datetime_src = time.strptime(string_time_src, '%Y-%m-%d')
        datetime_dst = time.strptime(string_time_dst, '%Y-%m-%d')
        # 从时间数据结构转换成时间戳
        timestamp_src = time.mktime(datetime_src)
        timestamp_dst = time.mktime(datetime_dst)

        # 时间戳可以直接相减，得到以秒为单位的差额
        time_diff = timestamp_src - timestamp_dst

        logging.info("time diff:" + str(time_diff))

        return time_diff

    def cac_time_diff_with_current_by_str(self, string_time):
        str_date_time = self.get_now_day_str()
        time_diff = self.cac_time_diff_by_str(string_time, str_date_time)

        return time_diff

    def check_time_is_ok(self, string_time):
        time_diff = self.cac_time_diff_with_current_by_str(string_time)

        if time_diff > 0:
            return True
        else:
            return False
