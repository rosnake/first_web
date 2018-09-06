#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import json
from handlers.base import BaseHandler
from methods.controller import PageController  # 导入页面控制器
from methods.debug import *
from methods.toolkits import DateToolKits
from orm.attendance import AttendanceModule


# 继承 base.py 中的类 BaseHandler
class AdminAttendanceHandler(BaseHandler):
    """
    用户首页处理，显示一些客户不需要登陆也可查看的信息
    """

    @tornado.web.authenticated
    def get(self):
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()
        if self.session["authorized"] is None or self.session["authorized"] is False:
            self.redirect("/login?next=/admin/attendance")
            return

        page_controller = PageController()
        render_controller = page_controller.get_render_controller()
        if self.session["authorized"] is None or self.session["authorized"] is False:
            self.redirect("/login?next=/admin/exchange")
            return

        username = self.get_current_user()

        print(self.session["authorized"])
        render_controller["index"] = False
        render_controller["authorized"] = self.session["authorized"]
        render_controller["login"] = False
        render_controller["admin"] = self.session["admin"]
        render_controller["organizer"] = self.session["organizer"]

        attendance_tables = self.__get_attendance_tables()

        if username is not None:
            self.render("admin/attendance.html",
                        attendance_tables=attendance_tables,
                        controller=render_controller,
                        username=username,
                        )

    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        operation = self.get_argument("operation")
        username = self.get_argument("username")
        uid = self.get_argument("id")
        role = self.get_argument("role")

        logging.info("operation:%s , username: %s, role:%s id: %s" % (operation, username, role, uid))

    def __get_attendance_tables(self):
        attendance_tables = []

        attendance_modules = AttendanceModule.get_all_attendance_info()

        if attendance_modules:
            for x in attendance_modules:
                tmp = {
                    "attendance_id": id, "username": x.username, "nickname": x.nickname,
                    "absence_reason": x.absence_reason, "absence_id": x.absence_id, "attend": x.attend,
                    "apply_time": x.apply_time, "datetime": x.datetime
                }
                attendance_tables.append(tmp)

        return attendance_tables
