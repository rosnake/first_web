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
            current_point = self.__get_current_point(user_name)
            presents_table = self.__get_presents_table(current_point)
            self.render("statistics.html", current_point=current_point, history_table=history_table,
                        controller=self.render_controller, user_name=user_name, point_stat=point_stat,
                        presents_table=presents_table)

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

        if __current:
            logging.info("current point [%d]" % __current.current_point)
            return __current.current_point

        else:
            logging.info("current point [0]")
            return 0

    def __get_point_history_by_user_name(self, user_name):
        history_module = self.db.query(ScoringHistoryModule).filter(ScoringHistoryModule.user_name == user_name).all()

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
        history_module = self.db.query(ScoringHistoryModule).filter(ScoringHistoryModule.user_name == user_name).all()
        mark_module = ScoringCriteriaModule.get_all_scoring_criteria()
        user_point = dict()
        user_point.update({"user_name": user_name})
        if history_module and mark_module:
            for x in mark_module:
                point = 0
                for y in history_module:
                    if x.id == y.mark_id:
                        point = point + y.points
                        user_point.update({x.markname: point})

            return user_point

        else:
            return user_point

    def __get_presents_table(self, current_point):
        exchange_rules = ExchangeRulesModule.get_all_exchange_rules()

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
        present_min_points = self.db.query(ExchangeRulesModule).filter(ExchangeRulesModule.id == present_id).first()

        if present_min_points is None:
            logging.info("present min point is None")
            return False

        current = self.__get_current_point(user_name)
        if current < present_min_points.min_points:
            logging.info("current point [%d], need point [%d]" % (current, present_min_points.min_points))
            return False

        exchanged_modules = self.db.query(ExchangeApplyModule).filter(ExchangeApplyModule.user_name == user_name).\
            filter(ExchangeApplyModule.exchange_accept == False).all()
        exchanged_point = 0
        if exchanged_modules:
            for x in exchanged_modules:
                exchanged_point = exchanged_point + x.need_points

        logging.info("current point [%d], exchanged point [%d]" % (current, exchanged_point))
        current_point = current - exchanged_point

        if current_point < present_min_points.min_points:
            logging.info("current point [%d], need point [%d]" % (current_point, present_min_points.min_points))

            return False

        date_kits = DateToolKits()
        exchange_apply = ExchangeApplyModule()
        exchange_apply.exchange_accept = False
        exchange_apply.exchange_status = "apply"
        exchange_apply.user_name = user_name
        exchange_apply.current_score = current
        exchange_apply.exchange_item = present_min_points.exchange_rule_name
        exchange_apply.datetime = date_kits.get_now_time()
        exchange_apply.need_points = present_min_points.exchange_rule_points
        self.db.add(exchange_apply)
        self.db.commit()
        return True

