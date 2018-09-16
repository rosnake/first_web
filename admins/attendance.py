#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import json
from handlers.base import BaseHandler
from methods.controller import PageController  # 导入页面控制器
from methods.debug import *
from methods.toolkits import DateToolKits
from orm.attendance import AttendanceModule
from orm.points import PointsModule
from orm.marks import MarksModule


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
        absent_id = self.get_argument("absent_id", -1)

        logging.info("operation:%s , username: %s" % (operation, username))

        if operation == "leave_accept":
            ret = self.__set_attendance_leave_accept_by_username(username)
            if ret is True:
                response["status"] = True
                response["message"] = "处理成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "签到失败"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

        if operation == "leave_reject":
            ret = self.__set_attendance_leave_reject_by_username(username)
            if ret is True:
                response["status"] = True
                response["message"] = "处理成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "签到失败"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

        if operation == "sign":
            ret = self.__attendance_sign_by_username(username)
            if ret is True:
                response["status"] = True
                response["message"] = "处理成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "签到失败"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

        if operation == "absent":
            ret = self.__set_attendance_absent_by_username(username, absent_id)
            if ret is True:
                response["status"] = True
                response["message"] = "处理成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "签到失败"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

    def __set_attendance_absent_by_username(self, username, absent_id):
        attendance = self.db.query(AttendanceModule).filter(AttendanceModule.username == username).first()

        if attendance is not None:
            deduct = self.db.query(MarksModule).filter(MarksModule.id == attendance.absence_id).first()
            #  更新积分表
            user_point = self.db.query(PointsModule).filter(PointsModule.username == username).first()

            if user_point and deduct:
                self.db.query(PointsModule).filter(PointsModule.username == username).update({
                    PointsModule.last_point: user_point.current_point,
                    PointsModule.current_point: user_point.current_point + deduct.points,
                })
                self.db.commit()
            else:
                return False

            self.db.query(AttendanceModule).filter(AttendanceModule.username == username).update({
                AttendanceModule.signed: True,
                AttendanceModule.attend: True,
                AttendanceModule.absent_accept: True,

            })
            self.db.commit()
            logging.info("modify attendance succeed")
            return True
        else:
            logging.error("modify attendance failed")
            return False

    def __attendance_sign_by_username(self, username):
        attendance = self.db.query(AttendanceModule).filter(AttendanceModule.username == username).first()

        if attendance is not None:
            self.db.query(AttendanceModule).filter(AttendanceModule.username == username).update({
                AttendanceModule.signed: True,
                AttendanceModule.attend: True,
                AttendanceModule.absent_accept: False,
            })
            self.db.commit()
            logging.info("modify attendance succeed")
            return True
        else:
            logging.error("modify attendance failed")
            return False

    def __set_attendance_leave_accept_by_username(self, username):
        attendance = self.db.query(AttendanceModule).filter(AttendanceModule.username == username).first()

        if attendance is not None:
            deduct = self.db.query(MarksModule).filter(MarksModule.id == attendance.absence_id).first()
            #  更新积分表
            user_point = self.db.query(PointsModule).filter(PointsModule.username == username).first()

            if user_point and deduct:
                self.db.query(PointsModule).filter(PointsModule.username == username).update({
                    PointsModule.last_point: user_point.current_point,
                    PointsModule.current_point: user_point.current_point + deduct.points,
                })
                self.db.commit()
            else:
                return False

            self.db.query(AttendanceModule).filter(AttendanceModule.username == username).update({
                AttendanceModule.signed: True,
                AttendanceModule.attend: True,
                AttendanceModule.absent_accept: True,

            })
            self.db.commit()
            logging.info("modify attendance succeed")
            return True
        else:
            logging.error("modify attendance failed")
            return False

    def __set_attendance_leave_reject_by_username(self, username):
        attendance = self.db.query(AttendanceModule).filter(AttendanceModule.username == username).first()

        if attendance is not None:
            self.db.query(AttendanceModule).filter(AttendanceModule.username == username).update({
                AttendanceModule.signed: False,
                AttendanceModule.attend: True,
                AttendanceModule.absent_accept: False,
            })
            self.db.commit()
            logging.info("modify attendance succeed")
            return True
        else:
            logging.error("modify attendance failed")
            return False

    def __get_attendance_tables(self):
        attendance_tables = []

        attendance_modules = AttendanceModule.get_all_attendance_info()

        if attendance_modules:
            for x in attendance_modules:
                tmp = {
                    "attendance_id": id, "username": x.username, "nickname": x.nickname,"signed": x.signed,
                    "absence_reason": x.absence_reason, "absence_id": x.absence_id, "attend": x.attend,
                    "apply_time": x.apply_time, "datetime": x.datetime,"absent_accept": x.absent_accept,
                }
                attendance_tables.append(tmp)

        return attendance_tables
