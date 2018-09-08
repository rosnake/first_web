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
        pass

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
