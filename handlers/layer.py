#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
from handlers.base import BaseHandler
import json
from methods.debug import *
import sys
from methods.utils import UserDataUtils
from orm.history import HistoryModule
from orm.marks import MarksModule


class LayerHandler(BaseHandler):
    """
    该类主要用户处理弹出页面以及弹出页面相关操作。
    1、根据用户提供的信息在数据库查询后显示相应的编辑窗口
    2、根据用户编辑后的提交信息，写如数据库，并返回相关状态
    """

    def get(self):
        if self.session["authorized"] is None or self.session["authorized"] is False:
            self.redirect("/login?next=/home")
            return

        username = self.get_argument("user", "unknown")
        operation = self.get_argument("operation", "unknown")

        if username == "unknown" or operation == "unknown":
            logging.error("popup layer username:"+username+" operation:" + operation)
            self.redirect("/")
            return

        if operation == "detail_browse":
            history_table = self.__get_point_history_by_user_name(username)
            point_stat = self.__get_point_stat_by_user_name(username)
            self.render("detail_browse.html", history_table=history_table, point_stat=point_stat)

            return

        if operation == "absent_apply":
            if self.session["username"] == username:
                leave_reason = self.__get_all_leave_reason()
                self.render("absent_apply.html", username=username, leave_reason=leave_reason)

    def post(self):
        ret = {"status": True, "data": "", "error": "succeed"}
        username = self.get_argument("username")
        password = self.get_argument("password")

        print("username:%s password:%s " % (username, password))

        succeed = True
        if (succeed):
            debug_msg(LayerHandler, sys._getframe().f_lineno, "redirect home page")
            # self.render("home.html")
            self.write(json.dumps(ret))
        else:
            debug_msg(LayerHandler, sys._getframe().f_lineno, "错误处理")
            # self.render("home.html")
            ret["status"] = False
            ret["error"] = "密码错误！"
            self.write(json.dumps(ret))

    def __get_point_history_by_user_name(self, user_name):
        history_module = self.db.query(HistoryModule).filter(HistoryModule.user_name == user_name).all()

        history_table = []
        if history_module:
            for history in history_module:
                tmp = {
                    "transactor": history.transactor, "mark_name": history.mark_name,
                    "points": history.points, "datetime": history.datetime,
                }
                history_table.append(tmp)

            return history_table
        else:
            return history_table

    def __get_point_stat_by_user_name(self, user_name):
        history_module = self.db.query(HistoryModule).filter(HistoryModule.user_name == user_name).all()
        mark_module = MarksModule.get_all_marks()

        user_point = {}
        user_point["username"] = user_name
        if history_module and mark_module:
            user_point = {}
            for x in mark_module:
                point = 0
                for y in history_module:
                    if x.id == y.mark_id:
                        point = point + y.points

                        user_point[x.markname] = point

            return user_point

        else:
            return user_point

    def __get_all_leave_reason(self):
        deduct_module = MarksModule.get_all_marks()

        leave_reason = []

        if deduct_module:
            for x in deduct_module:
                if x.points < 0:
                    tmp = {"reason_id": x.id, "leave_reason": x.markname}
                    leave_reason.append(tmp)

            return leave_reason
        else:
            return leave_reason



