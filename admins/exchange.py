#!/usr/bin/env Python
# coding=utf-8

import json
from handlers.base import BaseHandler
from methods.toolkits import DateToolKits
from orm.rules import ExchangeRuleModule
from methods.debug import *
from orm.exchange import ExchangeModule
from orm.points import PointsModule
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth


# 继承 base.py 中的类 BaseHandler
class AdminExchangeHandler(BaseHandler):
    """
    用户积分兑换管理
    """

    @admin_get_auth("/admin/exchange", True)
    def get(self):
        username = self.get_current_user()

        if username is not None:
            user_exchange_tables = self.__get_all_exchange_tables()
            exchange_rule_tables = self.__get_all_exchange_rules()

            self.render("admin/exchange.html",
                        user_exchange_tables=user_exchange_tables,
                        exchange_rule_tables=exchange_rule_tables,
                        controller=self.render_controller,
                        username=username,
                        )

    @admin_post_auth(False)
    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        response["data"] = date_kits.get_now_day_str()
        rule_name = "none"
        rule_id = 0
        need_points = 0
        min_points = 0
        exchange_id = 0
        user_name = "none"
        operation = self.get_argument("operation")

        if operation == "exchange_reject" or operation == "exchange_confirm":
            exchange_id = self.get_argument("exchange_id")
            user_name = self.get_argument("user_name")
        else:
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

        if operation == "exchange_confirm":
            ret = self.__exchange_item_confirm(exchange_id, user_name)
            if ret is True:
                response["status"] = True
                response["message"] = "兑换成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "兑换失败"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

        if operation == "exchange_reject":
            ret = self.__exchange_item_reject(exchange_id)
            if ret is True:
                response["status"] = True
                response["message"] = "取消兑换成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "取消兑换失败"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

    def __get_all_exchange_rules(self):
        exchange_rule_module = ExchangeRuleModule.get_all_exchange_rules()
        exchange_rule_tables = []
        if exchange_rule_module:
            for module in exchange_rule_module:
                rule = {"rule_id": module.id, "rule_name": module.exchange_rule_name,
                        "need_points": module.exchange_rule_points, "points_range": module.min_points}
                exchange_rule_tables.append(rule)

        return exchange_rule_tables

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

    def __get_all_exchange_tables(self):
        exchange_modules = ExchangeModule.get_all_exchange()
        exchange_table = []

        if exchange_modules:
            for x in exchange_modules:
                tmp = {"exchange_id": x.id, "user_name": x.user_name, "user_points": x.current_points,
                       "exchange_item": x.exchange_item, "apply_date": x.datetime, "exchanged": x.exchange_finish}
                exchange_table.append(tmp)

        return exchange_table

    def __exchange_item_confirm(self, exchange_id, user_name):
        exchange_modules = self.db.query(ExchangeModule).filter(ExchangeModule.id == exchange_id).first()
        point_modules = self.db.query(PointsModule).filter(PointsModule.username == user_name).first()
        if exchange_modules and point_modules:
            self.db.query(ExchangeModule).filter(ExchangeModule.id == exchange_id).update({
                ExchangeModule.exchange_finish: True,
                ExchangeModule.exchange_status: "confirm",
            })
            self.db.commit()

            self.db.query(PointsModule).filter(PointsModule.username == user_name).update({
                PointsModule.current_point: point_modules.current_point - exchange_modules.need_points,
            })
            self.db.commit()

            exchange_all = self.db.query(ExchangeModule).filter(ExchangeModule.user_name == user_name).all()
            con = False
            for x in exchange_all:
                self.db.query(ExchangeModule).filter(ExchangeModule.user_name == user_name).filter(
                    ExchangeModule.exchange_finish == con).update({ExchangeModule.current_points: point_modules.current_point - exchange_modules.need_points})
                self.db.commit()

            return True

        else:
            return False

    def __exchange_item_reject(self, exchange_id):
        exchange_modules = self.db.query(ExchangeModule).filter(ExchangeModule.id == exchange_id).first()
        if exchange_modules:
            self.db.query(ExchangeModule).filter(ExchangeModule.id == exchange_id).update({
                ExchangeModule.exchange_finish: True,
                ExchangeModule.exchange_status: "reject",
            })
            self.db.commit()
            return True
        else:
            return False

