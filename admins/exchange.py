#!/usr/bin/env Python
# coding=utf-8

import json
import tornado.escape
from handlers.base import BaseHandler
from methods.utils import UserDataUtils
from methods.utils import UserAuthUtils
from methods.toolkits import DateToolKits
from methods.controller import PageController
from orm.rules import ExchangeRuleModule
from methods.debug import *


# 继承 base.py 中的类 BaseHandler
class AdminExchangeHandler(BaseHandler):
    """
    用户首页处理，显示一些客户不需要登陆也可查看的信息
    """
    def get(self):
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

        if username is not None:
            user_exchange_tables = UserDataUtils.get_user_exchange_tables()  # 后续需要用数据库替换
            exchange_rule_module = ExchangeRuleModule.get_all_exchange_rules()
            exchange_rule_tables = []
            self.__convert_module_to_table(exchange_rule_module, exchange_rule_tables)

            self.render("admin/exchange.html",
                        user_exchange_tables=user_exchange_tables,
                        exchange_rule_tables=exchange_rule_tables,
                        controller=render_controller,
                        username=username,
                        )

    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        response["data"] = date_kits.get_now_day_str()

        operation = self.get_argument("operation")
        rule_name = self.get_argument("rule_name")
        rule_id = self.get_argument("id")
        need_points = self.get_argument("need_points")
        min_points = self.get_argument("min_points")

        if operation == "add":
            ret = self.__add_exchange_rule(rule_name, need_points, min_points)
            if ret is True:
                response["status"] = True
                response["message"] = "新增成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "当前积分规则已存在"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

        if operation == "delete":
            ret = self.__delete_rule_by_id(rule_id)
            if ret is True:
                response["status"] = True
                response["message"] = "删除成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "当前积分规则不支持"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

        if operation == "modify":
            ret = self.__modify_rule_by_id(rule_id, need_points, min_points)
            if ret is True:
                response["status"] = True
                response["message"] = "删除成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "当前用户已存在"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

    def __convert_module_to_table(self, exchange_rule_module, exchange_rule_tables):
        if exchange_rule_module is None:
            return False

        for module in exchange_rule_module:
            rule = {"rule_id": module.id, "rule_name": module.exchange_rule_name,
                    "need_points": module.exchange_rule_points, "points_range": module.min_points}
            exchange_rule_tables.append(rule)

        return True

    def __add_exchange_rule(self, rule_name, need_points, min_points):
        rule = self.db.query(ExchangeRuleModule).filter(ExchangeRuleModule.exchange_rule_name == rule_name).first()
        if rule is not None:
            logging.error("current exchange rule is exit")
            return False

        exchange_rule = ExchangeRuleModule()
        exchange_rule.exchange_rule_name = rule_name
        exchange_rule.exchange_rule_points = need_points
        exchange_rule.min_points = min_points
        self.db.add(exchange_rule)
        self.db.commit()
        return True

    def __delete_rule_by_id(self, rule_id):
        deduct = self.db.query(ExchangeRuleModule).filter(ExchangeRuleModule.id == rule_id).first()

        if deduct is not None:
            self.db.delete(deduct)
            self.db.commit()
            logging.info("delete exchange rule succeed")
            return True
        else:
            logging.error("delete exchange rule failed")
            return False

    def __modify_rule_by_id(self, rule_id, need_points, min_point):
        rule = self.db.query(ExchangeRuleModule).filter(ExchangeRuleModule.id == rule_id).first()

        if rule is not None:
            self.db.query(ExchangeRuleModule).filter(ExchangeRuleModule.id == rule_id).update({
                ExchangeRuleModule.exchange_rule_points: need_points,
                ExchangeRuleModule.min_points: min_point,
            })
            self.db.commit()
            logging.info("modify exchange rule succeed")
            return True
        else:
            logging.error("modify exchange rule failed")
            return False
