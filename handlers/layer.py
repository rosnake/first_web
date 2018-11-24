#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
import json
from methods.debug import *
import sys
from orm.score_history import ScoringHistoryModule
from orm.score_criteria import ScoringCriteriaModule
from handlers.decorator import handles_get_auth
from handlers.decorator import handles_post_auth

class LayerHandler(BaseHandler):
    """
    该类主要用户处理弹出页面以及弹出页面相关操作。
    1、根据用户提供的信息在数据库查询后显示相应的编辑窗口
    2、根据用户编辑后的提交信息，写如数据库，并返回相关状态
    """

    @handles_get_auth("/home")
    def get(self):
        user_name = self.get_argument("user", "unknown")
        operation = self.get_argument("operation", "unknown")

        if user_name == "unknown" or operation == "unknown":
            logging.error("popup layer user_name:"+user_name+" operation:" + operation)
            self.redirect("/")
            return

        if operation == "detail_browse":
            history_table = self.__get_point_history_by_user_name(user_name)
            point_stat = self.__get_point_stat_by_user_name(user_name)
            self.render("/handlers/detail_browse.html", history_table=history_table, point_stat=point_stat)

            return

        if operation == "absent_apply":
            if self.session["user_name"] == user_name:
                leave_reason = self.__get_all_leave_reason()
                self.render("handlers/absent_apply.html", user_name=user_name, leave_reason=leave_reason)

    @handles_post_auth
    def post(self):
        pass

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

        user_score = {}
        user = {'user_name': user_name}
        user_score.update(user)

        if history_module:
            if criteria_module:
                for criteria in criteria_module:
                    score = 0
                    for history in history_module:
                        if criteria.id == history.criteria_id:
                            score = score + history.score_value  # 根据历史记录计算当前项已扣分总数

                    criteria_score = {criteria.criteria_name: score}
                    user_score.update(criteria_score)

                return user_score

            else:
                return user_score
        else:
            if criteria_module:
                for criteria in criteria_module:
                    score = 0
                    criteria_score = {criteria.criteria_name: score}
                    user_score.update(criteria_score)

            return user_score

    def __get_all_leave_reason(self):
        criteria_module = ScoringCriteriaModule.get_all_scoring_criteria()

        leave_reason = []

        if criteria_module:
            for criteria in criteria_module:
                if criteria.score_value < 0:
                    tmp = {"reason_id": criteria.id, "leave_reason": criteria.criteria_name}
                    leave_reason.append(tmp)

            return leave_reason
        else:
            return leave_reason



