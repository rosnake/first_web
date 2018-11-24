#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from orm.score_info import ScoreInfoModule
from orm.score_history import ScoringHistoryModule
from orm.score_criteria import ScoringCriteriaModule
from orm.exchange_rules import ExchangeRulesModule
from methods.toolkits import DateToolKits
import json
from orm.exchange_apply import ExchangeApplyModule
from handlers.decorator import handles_get_auth
from handlers.decorator import handles_post_auth
from methods.debug import *
from orm.exchanged_history import ExchangedHistoryModule
# 继承 base.py 中的类 BaseHandler


class StatHandler(BaseHandler):
    """
    该类处理的主要是用户积分统计信息
    该类只有在登陆成功后才会显示主页页面，登陆失败，不显示该页面
    """

    @handles_get_auth("/statistics")
    def get(self):
        user_name = self.get_current_user()
        # 先判断是否完善其他信息，如果没有完善，跳转到信息完善页面
        if user_name is not None:
            history_table = self.__get_point_history_by_user_name(user_name)
            point_stat = self.__get_point_stat_by_user_name(user_name)
            user_exchange_tables = self.__get_current_user_exchange_tables(user_name)
            exchanged_history = self.__get_user_exchanged_history_by_username(user_name)
            # print(point_stat)
            current_scores = self.__get_current_point(user_name)
            presents_table = self.__get_presents_table(current_scores["exchange"])
            self.render("handlers/statistics.html", current_scores=current_scores, history_table=history_table,
                        controller=self.render_controller, user_name=user_name, point_stat=point_stat,
                        presents_table=presents_table,
                        language_mapping=self.language_mapping,
                        user_exchange_tables=user_exchange_tables,
                        exchanged_history=exchanged_history,
                        )

    @handles_post_auth
    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        response["data"] = date_kits.get_now_day_str()

        operation = self.get_argument("operation")
        #  present = self.get_argument("present")
        present_id = self.get_argument("present_id")

        user_name = self.get_current_user()

        if operation == "exchange":
            ret = self.__exchange_apply_by_user_name(user_name, present_id)
            if ret is True:
                response["status"] = True
                response["message"] = "申请成功！"
                response["data"] = date_kits.get_now_day_str()
                opt = "apply a exchange, username: " + user_name
                self.record_operation_history(user_name, opt)
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "积分兑换失败"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

    def __get_current_point(self, user_name):
        __current = self.db.query(ScoreInfoModule).filter(ScoreInfoModule.user_name == user_name).first()
        __exchange = self.db.query(ExchangeApplyModule).filter(ExchangeApplyModule.user_name == user_name).all()
        __current_scores = 0
        __exchange_score = 0
        __exchanged_score = 0

        if __current:
            logging.info("current point [%d]" % __current.current_scores)
            __current_scores = __current.current_scores
            if __exchange:
                for x in __exchange:
                    if x.exchange_accept is False:
                        __exchanged_score = __exchanged_score + x.need_score
                        logging.info("---->exchanged score:%d" % __exchanged_score)

            __exchange_score = __current_scores - __exchanged_score
            current_scores = {"current": __current_scores, "exchange": __exchange_score}
        else:
            current_scores = {"current": 0, "exchange": 0}

        logging.info("current total score:%d, exchanged score:%d,current exchange available score:%d"
                     % (__current_scores, __exchanged_score, __exchange_score))
        return current_scores

    def __get_point_history_by_user_name(self, user_name):
        history_module = self.db.query(ScoringHistoryModule).filter(ScoringHistoryModule.user_name == user_name).all()

        history_table = []
        if history_module:
            for history in history_module:
                tmp = {
                    "transactor": history.transactor, "mark_name": history.criteria_name,
                    "points": history.score_value, "datetime": history.date_time,
                }
                history_table.append(tmp)

            return history_table
        else:
            return history_table

    def __get_point_stat_by_user_name(self, user_name):
        history_module = self.db.query(ScoringHistoryModule).filter(ScoringHistoryModule.user_name == user_name).all()
        criteria_module = ScoringCriteriaModule.get_all_scoring_criteria()
        user_point = dict()

        if history_module and criteria_module:
            for criteria in criteria_module:
                point = 0
                for history in history_module:
                    if criteria.id == history.criteria_id:
                        logging.info("history id %s, criteria id:%s" % (history.criteria_id, criteria.id))
                        point = point + history.score_value
                        user_point.update({criteria.criteria_name: point})

            return user_point

        else:
            logging.error("history or criteria is none,return none")
            return user_point

    def __get_presents_table(self, current_scores):
        exchange_rules = ExchangeRulesModule.get_all_exchange_rules()

        presents_table = []
        if exchange_rules:
            for x in exchange_rules:
                if current_scores >= x.exchange_min_score:
                    tmp = {
                        "present_id": x.id, "present_name": x.exchange_rule_name,
                        "consume_point": x.exchange_rule_score, "exchange_min_score": x.exchange_min_score
                    }

                    presents_table.append(tmp)

            return presents_table

        else:
            return presents_table

    def __exchange_apply_by_user_name(self, user_name, present_id):
        present_exchange = self.db.query(ExchangeRulesModule).filter(ExchangeRulesModule.id == present_id).first()

        # 1、判断规则是否存在
        if present_exchange is None:
            logging.info("present min point is None")
            return False
        # 2、判断当前可兑换积分是否满足当前需要兑换物品的最小积分
        current = self.__get_current_point(user_name)
        if current["exchange"] < present_exchange.exchange_min_score:
            logging.info("current point [%d], need point [%d]"
                         % (current["exchange"], present_exchange.exchange_min_score))
            return False

        logging.info("current point [%d], exchanged point [%d]" % (current["current"], current["exchange"]))

        date_kits = DateToolKits()
        exchange_apply = ExchangeApplyModule()
        exchange_apply.exchange_accept = False
        exchange_apply.exchange_status = "apply"
        exchange_apply.user_name = user_name
        exchange_apply.current_scores = current["current"]
        exchange_apply.exchange_item = present_exchange.exchange_rule_name
        exchange_apply.datetime = date_kits.get_now_time()
        exchange_apply.need_score = present_exchange.exchange_rule_score
        self.db.add(exchange_apply)
        self.db.commit()
        return True

    def __get_current_user_exchange_tables(self, user_name):
        exchange_modules = self.db.query(ExchangeApplyModule).filter(ExchangeApplyModule.user_name == user_name).all()
        exchange_table = []

        if exchange_modules:
            logging.info("exchange modules is not null")
            for exchange in exchange_modules:
                tmp = {"exchange_id": exchange.id, "user_name": exchange.user_name,
                       "user_points": exchange.current_scores, "exchange_item": exchange.exchange_item,
                       "apply_date": exchange.date_time, "exchanged": exchange.exchange_accept}
                exchange_table.append(tmp)
        else:
            logging.info("exchange modules is null")
        return exchange_table

    def __get_user_exchanged_history_by_username(self, user_name):
        exchangeds = self.db.query(ExchangedHistoryModule).filter(ExchangedHistoryModule.user_name == user_name).all()
        exchanged_history = []

        if exchangeds:
            logging.info("exchanged history is not null")
            for exchanged in exchangeds:
                tmp = {"history_id": exchanged.id, "user_name": exchanged.user_name,
                       "exchange_rule_name": exchanged.exchange_rule_name,
                       "exchange_rule_score": exchanged.exchange_rule_score,
                       "exchanged_transactor": exchanged.exchanged_transactor,
                       "exchanged_date_time": exchanged.exchanged_date_time}

                exchanged_history.append(tmp)
        else:
            logging.info("exchanged history modules is null")

        return exchanged_history
