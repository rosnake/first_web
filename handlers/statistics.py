#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
from handlers.base import BaseHandler
from methods.utils import UserDataUtils
from  methods.utils import UserAuthUtils
from methods.debug import *
from methods.controller import PageController
from orm.points import PointsModule
from orm.history import HistoryModule
from orm.marks import MarksModule
from orm.rules import ExchangeRuleModule
from methods.toolkits import DateToolKits
import json
from orm.exchange import ExchangeModule

# 继承 base.py 中的类 BaseHandler


class StatHandler(BaseHandler):
    """
    该类处理的主要是登陆后显示的主页和基于主页的操作
    该类只有在登陆成功后才会显示主页页面，登陆失败，不显示该页面
    """

    @tornado.web.authenticated
    def get(self):
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()
        if self.session["authorized"] is None or self.session["authorized"] is False:
            self.redirect("/login?next=/statistics")
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
            history_table = self.__get_point_history_by_user_name(username)
            point_stat = self.__get_point_stat_by_user_name(username)
            current_point = self.__get_current_point(username)
            presents_table = self.__get_presents_table(current_point)
            self.render("statistics.html", current_point=current_point, history_table=history_table,
                        controller=render_controller, username=username, point_stat=point_stat,
                        presents_table=presents_table)

    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        response["data"] = date_kits.get_now_day_str()

        operation = self.get_argument("operation")
        #  present = self.get_argument("present")
        present_id = self.get_argument("present_id")

        username = self.get_current_user()

        if operation == "exchange":
            ret = self.__exchange_apply_by_user_name(username, present_id)
            if ret is True:
                response["status"] = True
                response["message"] = "申请成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "积分兑换失败"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

    def __get_current_point(self, username):
        __current = self.db.query(PointsModule).filter(PointsModule.username == username).first()

        if __current:
            return __current.current_point
        else:
            return 0

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

    def __get_presents_table(self, current_point):
        exchange_rules = ExchangeRuleModule.get_all_exchange_rules()

        presents_table = []
        if exchange_rules:
            for x in exchange_rules:
                if current_point >= x.min_points:
                    tmp = {
                        "present_id": x.id, "present_name": x.exchange_rule_name,
                        "consume_point": x.exchange_rule_points, "min_points": x.min_points
                    }

                    presents_table.append(tmp)

            return presents_table

        else:
            return presents_table

    def __exchange_apply_by_user_name(self, user_name, present_id):
        present_min_points = self.db.query(ExchangeRuleModule).filter(ExchangeRuleModule.id == present_id).first()

        if present_min_points is None:
            return False

        current = self.__get_current_point(user_name)
        if current < present_min_points.min_points:
            return False

        exchanged_modules = self.db.query(ExchangeModule).filter(ExchangeModule.user_name == user_name).all()
        exchanged_point = 0
        if exchanged_modules:
            for x in exchanged_modules:
                exchanged_point = exchanged_point + x.need_points

        current_point = current - exchanged_point

        if current_point < present_min_points.min_points:
            return False

        date_kits = DateToolKits()
        exchange_apply = ExchangeModule()
        exchange_apply.exchange_finish = False
        exchange_apply.exchange_status = "apply"
        exchange_apply.user_name = user_name
        exchange_apply.current_points = current
        exchange_apply.exchange_item = present_min_points.exchange_rule_name
        exchange_apply.datetime = date_kits.get_now_time()
        exchange_apply.need_points = present_min_points.exchange_rule_points
        self.db.add(exchange_apply)
        self.db.commit()
        return True

