#!/usr/bin/env Python
# coding=utf-8

import json
from handlers.base import BaseHandler
from methods.toolkits import DateToolKits
from orm.exchange_rules import ExchangeRulesModule
from methods.debug import *
from orm.exchange_apply import ExchangeApplyModule
from orm.score_info import ScoreInfoModule
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth
from orm.operation_history import OperationHistoryModule


# 继承 base.py 中的类 BaseHandler
class AdminExchangeHandler(BaseHandler):
    """
    用户积分兑换管理
    """

    @admin_get_auth("/admin/exchange", True)
    def get(self):
        user_name = self.get_current_user()

        if user_name is not None:
            user_exchange_tables = self.__get_all_exchange_tables()
            exchange_rule_tables = self.__get_all_exchange_rules()

            self.render("admin/exchange.html",
                        user_exchange_tables=user_exchange_tables,
                        exchange_rule_tables=exchange_rule_tables,
                        controller=self.render_controller,
                        user_name=user_name,
                        language_mapping=self.language_mapping,
                        )

    @admin_post_auth(False)
    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        response["data"] = date_kits.get_now_day_str()
        rule_name = "none"
        rule_id = 0
        need_score = 0
        exchange_min_score = 0
        exchange_id = 0
        user_name = "none"
        operation = self.get_argument("operation")

        if operation == "exchange_reject" or operation == "exchange_confirm":
            exchange_id = self.get_argument("exchange_id")
            user_name = self.get_argument("user_name")
        else:
            rule_name = self.get_argument("rule_name")
            rule_id = self.get_argument("id")
            need_score = self.get_argument("need_score")
            exchange_min_score = self.get_argument("exchange_min_score")
            logging.info(" rule_name:"+rule_name+" rule_id:"+rule_id+" need_score:"+need_score+" exchange_min_score:"+exchange_min_score)

        if operation == "add":
            ret = self.__add_exchange_rule(rule_name, need_score, exchange_min_score)
            if ret is True:
                response["status"] = True
                response["message"] = "新增成功！"
                response["data"] = date_kits.get_now_day_str()
                opt = "add exchange rule: " + rule_name
                self.record_operation_history(self.session["user_name"], opt)
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

                opt = "delete exchange rule"
                self.record_operation_history(self.session["user_name"], opt)
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "当前积分规则不支持"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

        if operation == "modify":
            ret = self.__modify_rule_by_id(rule_id, need_score, exchange_min_score)
            if ret is True:
                response["status"] = True
                response["message"] = "删除成功！"
                response["data"] = date_kits.get_now_day_str()
                opt = "modify exchange rule"
                self.record_operation_history(self.session["user_name"], opt)
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
                opt = "confirm exchanged,id:"+exchange_id
                self.record_operation_history(user_name, opt)
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
                opt = "reject exchanged,id:"+exchange_id
                self.record_operation_history(user_name, opt)
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "取消兑换失败"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

    def __get_all_exchange_rules(self):
        exchange_rule_module = ExchangeRulesModule.get_all_exchange_rules()
        exchange_rule_tables = []
        if exchange_rule_module:
            for module in exchange_rule_module:
                rule = {"rule_id": module.id, "rule_name": module.exchange_rule_name,
                        "need_score": module.exchange_rule_score, "points_range": module.exchange_min_score}
                exchange_rule_tables.append(rule)

        return exchange_rule_tables

    def __add_exchange_rule(self, rule_name, need_score, exchange_min_score):
        rule = self.db.query(ExchangeRulesModule).filter(ExchangeRulesModule.exchange_rule_name == rule_name).first()
        if rule is not None:
            logging.error("current exchange rule is exit")
            return False

        exchange_rule = ExchangeRulesModule()
        exchange_rule.exchange_rule_name = rule_name
        exchange_rule.exchange_rule_score = need_score
        exchange_rule.exchange_min_score = exchange_min_score
        self.db.add(exchange_rule)
        self.db.commit()
        return True

    def __delete_rule_by_id(self, rule_id):
        discipline = self.db.query(ExchangeRulesModule).filter(ExchangeRulesModule.id == rule_id).first()

        if discipline is not None:
            self.db.delete(discipline)
            self.db.commit()
            logging.info("delete exchange rule succeed")
            return True
        else:
            logging.error("delete exchange rule failed")
            return False

    def __modify_rule_by_id(self, rule_id, need_score, min_point):
        rule = self.db.query(ExchangeRulesModule).filter(ExchangeRulesModule.id == rule_id).first()

        if rule is not None:
            self.db.query(ExchangeRulesModule).filter(ExchangeRulesModule.id == rule_id).update({
                ExchangeRulesModule.exchange_rule_score: need_score,
                ExchangeRulesModule.exchange_min_score: min_point,
            })
            self.db.commit()
            logging.info("modify exchange rule succeed")
            return True
        else:
            logging.error("modify exchange rule failed")
            return False

    def __get_all_exchange_tables(self):
        exchange_modules = ExchangeApplyModule.get_all_exchange_apply_info()
        exchange_table = []

        if exchange_modules:
            for exchange in exchange_modules:
                tmp = {"exchange_id": exchange.id, "user_name": exchange.user_name,
                       "user_points": exchange.current_scores, "exchange_item": exchange.exchange_item,
                       "apply_date": exchange.date_time, "exchanged": exchange.exchange_accept}
                exchange_table.append(tmp)

        return exchange_table

    def __exchange_item_confirm(self, exchange_id, user_name):
        exchange_modules = self.db.query(ExchangeApplyModule).filter(ExchangeApplyModule.id == exchange_id).first()
        point_modules = self.db.query(ScoreInfoModule).filter(ScoreInfoModule.user_name == user_name).first()
        if exchange_modules and point_modules:
            # 更新扣分信息表
            self.db.query(ExchangeApplyModule).filter(ExchangeApplyModule.id == exchange_id).update({
                ExchangeApplyModule.exchange_accept: True,
                ExchangeApplyModule.exchange_status: "confirm",
            })
            logging.info("confirm %s exchange by id %s" % (user_name, exchange_id))
            self.db.commit()

            current_score = point_modules.current_scores - exchange_modules.need_score
            logging.info("current score info:%d" % current_score)
            # 更新用户积分信息
            logging.info("current scores %d, need scores %d" % (point_modules.current_scores, exchange_modules.need_score))
            self.db.query(ScoreInfoModule).filter(ScoreInfoModule.user_name == user_name).update({
                ScoreInfoModule.current_scores: current_score,
            })
            self.db.commit()

            # 更新未兑换的积分信息
            exchange_all = self.db.query(ExchangeApplyModule).filter(ExchangeApplyModule.user_name == user_name).all()
            for exchange in exchange_all:
                if exchange.exchange_accept is False and exchange.user_name == user_name:
                    self.db.query(ExchangeApplyModule).filter(ExchangeApplyModule.id == exchange.id).update({
                            ExchangeApplyModule.current_scores: current_score,
                        })
                    self.db.commit()

            return True

        else:
            return False

    def __exchange_item_reject(self, exchange_id):
        exchange_modules = self.db.query(ExchangeApplyModule).filter(ExchangeApplyModule.id == exchange_id).first()
        if exchange_modules:
            self.db.query(ExchangeApplyModule).filter(ExchangeApplyModule.id == exchange_id).update({
                ExchangeApplyModule.exchange_accept: True,
                ExchangeApplyModule.exchange_status: "reject",
            })
            self.db.commit()
            return True
        else:
            return False

