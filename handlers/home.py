#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import json
from handlers.base import BaseHandler
from methods.debug import *
from orm.user import UserModule
from methods.controller import PageController
from orm.topics import TopicsModule
from orm.points import PointsModule
from methods.toolkits import DateToolKits
from orm.marks import MarksModule
from orm.attendance import AttendanceModule


#继承 base.py 中的类 BaseHandler

class HomeHandler(BaseHandler):
    """
    该类处理的主要是登陆后显示的主页和基于主页的操作
    该类只有在登陆成功后才会显示主页页面，登陆失败，不显示该页面
    """

    @tornado.web.authenticated
    def get(self):
        # 用户渲染表格模板的数据接口
        # 后续该接口需要从数据库读取
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()
        if self.session["authorized"] is None or self.session["authorized"] is False:
            self.redirect("/login?next=/home")
            return

        username = self.get_current_user()

        print(self.session["authorized"])
        render_controller["index"] = False
        render_controller["authorized"] = self.session["authorized"]
        render_controller["login"] = False
        render_controller["admin"] = self.session["admin"]
        render_controller["organizer"] = self.session["organizer"]

        # 先判断是否完善其他信息，如果没有完善，跳转到信息完善页面
        if username is not None:
            user = self.db.query(UserModule).filter(UserModule.username == username).first()
            if user is not None:
                print(user.username)
                if user.email == "unknown":
                    self.redirect("/user?next=/home")
                    self.finish()
                    return

        points_table = self.__get_all_point_tables()
        topics_table = self.__get_all_topic_tables()

        self.render("home.html", points_table=points_table, controller=render_controller,
                    topics_table=topics_table, username=username)

    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        operation = self.get_argument("operation")
        username = self.get_argument("username")
        leave_id = self.get_argument("leave_id", 0)
        leave_date = self.get_argument("leave_date", "none")

        logging.info("operation:%s , username: %s, leave_id:%s leave_date: %s" % (operation, username, leave_id, leave_date))

        if operation == "leave_apply":
            ret = self.__leave_apply_by_id(username, leave_id, leave_date)

            if ret is True:
                response["status"] = True
                response["message"] = "申请成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
            else:
                response["status"] = False
                response["message"] = "申请失败！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))

            return

    def __leave_apply_by_id(self, username, leave_id, leave_date):
        mark = self.db.query(MarksModule).filter(MarksModule.id == leave_id).first()
        if mark is None:
            return False
        attendance = self.db.query(AttendanceModule).filter(AttendanceModule.username == username).first()

        if attendance is None:
            return False

        date_kits = DateToolKits()
        apply_time = date_kits.get_now_time()  # 申请时间

        self.db.query(AttendanceModule).filter(AttendanceModule.username == username).update({
            AttendanceModule.absence_reason: mark.markname,
            AttendanceModule.absence_id: mark.id,
            AttendanceModule.attend: False,
            AttendanceModule.apply_time: apply_time,
            AttendanceModule.datetime: leave_date,
        })

        self.db.commit()
        logging.info("user leave apply  succeed")

        return True

    def __get_all_topic_tables(self):
        topics_module = TopicsModule.get_all_topics()
        if topics_module is None:
            return None

        topics_tables = []
        for topics in topics_module:
            tmp = {
                "topic_id": topics.id, "name": topics.username, "image": topics.image, "title": topics.title,
                "current": topics.current, "finish": topics.finish, "time": topics.datetime,
                "description": topics.brief
            }
            topics_tables.append(tmp)

        return topics_tables

    def __get_all_point_tables(self):
        points_tables = []

        point_module = PointsModule.get_all_points()

        if point_module is None:
            return points_tables

        for point in point_module:
            tmp = {
                "user_name": point.username, "nick_name": point.nickname,
                "current_point": point.current_point, "last_point": point.last_point
            }
            points_tables.append(tmp)

        return points_tables

