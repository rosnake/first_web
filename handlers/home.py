#!/usr/bin/env Python
# coding=utf-8

import json
from handlers.base import BaseHandler
from methods.debug import *
from orm.users_info import UsersInfoModule
from orm.score_info import ScoreInfoModule
from methods.toolkits import DateToolKits
from orm.score_criteria import ScoringCriteriaModule
from orm.attendance import AttendanceModule
from handlers.decorator import handles_get_auth
from handlers.decorator import handles_post_auth


#继承 base.py 中的类 BaseHandler

class HomeHandler(BaseHandler):
    """
    该类处理的主要是登陆后显示的主页和基于主页的操作
    该类只有在登陆成功后才会显示主页页面，登陆失败，不显示该页面
    """

    @handles_get_auth("/home")
    def get(self):
        user_name = self.get_current_user()

        # 先判断是否完善其他信息，如果没有完善，跳转到信息完善页面
        if user_name is not None:
            user = self.db.query(UsersInfoModule).filter(UsersInfoModule.user_name == user_name).first()
            if user is not None:
                print(user.user_name)
                if user.email == "unknown":
                    self.redirect("/user?next=/home")
                    self.finish()
                    return

        points_table = self.__get_all_point_tables()

        self.render("home.html", points_table=points_table, controller=self.render_controller, user_name=user_name)

    @handles_post_auth
    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        operation = self.get_argument("operation")
        user_name = self.get_argument("user_name")
        leave_id = self.get_argument("leave_id", 0)
        leave_date = self.get_argument("leave_date", "none")

        logging.info("operation:%s , user_name: %s, leave_id:%s leave_date: %s" % (operation, user_name, leave_id, leave_date))

        if operation == "absent_apply":
            ret = self.__leave_apply_by_id(user_name, leave_id, leave_date)

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

    def __leave_apply_by_id(self, user_name, leave_id, leave_date):
        mark = self.db.query(ScoringCriteriaModule).filter(ScoringCriteriaModule.id == leave_id).first()
        if mark is None:
            return False
        attendance = self.db.query(AttendanceModule).filter(AttendanceModule.user_name == user_name).first()

        if attendance is None:
            return False

        date_kits = DateToolKits()
        apply_time = date_kits.get_now_time()  # 申请时间

        self.db.query(AttendanceModule).filter(AttendanceModule.user_name == user_name).update({
            AttendanceModule.absence_reason: mark.markname,
            AttendanceModule.absence_id: mark.id,
            AttendanceModule.attended: False,
            AttendanceModule.absence_apply_accept: False,
            AttendanceModule.absence_apply_time: apply_time,
            AttendanceModule.date_time: leave_date,
        })

        self.db.commit()
        logging.info("user leave apply  succeed")

        return True

    def __get_all_point_tables(self):
        points_tables = []

        point_module = ScoreInfoModule.get_all_score_info()

        if point_module is None:
            return points_tables

        for point in point_module:
            tmp = {
                "user_name": point.user_name, "nick_name": point.nick_name,
                "current_point": point.current_point, "last_point": point.last_point
            }
            points_tables.append(tmp)

        return points_tables

