#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from orm.issues_info import IssuesInfoModule
from orm.evaluation_info import EvaluationInfoModule
from handlers.decorator import handles_get_auth
from handlers.decorator import handles_post_auth
from methods.toolkits import DateToolKits
from methods.debug import *
import json


# 继承 base.py 中的类 BaseHandler
class TopicsHistoryHandler(BaseHandler):
    """
    用户议题显示处理
    """
    @handles_get_auth("/topics/history")
    def get(self):
        user_name = self.get_current_user()

        if user_name is not None:
            user_topic_tables = self.__get_history_issues_info()
            self.render("handlers/topic_history.html",
                        controller=self.render_controller,
                        user_name=user_name,
                        topics_table=user_topic_tables,
                        language_mapping=self.language_mapping,
                        )

    @handles_post_auth
    def post(self):
        pass

    def __get_history_issues_info(self):
        issues_module = IssuesInfoModule.get_all_issues_info()
        if issues_module is None:
            return None

        issues_tables = []
        for issues in issues_module:
            if issues.finish is True and issues.issues_evaluate_finish is True:
                tmp = {
                    "issues_id": issues.id, "keynote_user_name": issues.user_name, "issues_image": issues.issues_image,
                    "issues_title": issues.issues_title, "keynote_chinese_name": issues.chinese_name,
                    "current": issues.current, "finish": issues.finish,  "date_time": issues.expect_date_time,
                    "issues_brief": issues.issues_brief, "issues_score": issues.issues_score,
                    "issues_meeting_room": issues.issues_meeting_room, "actual_date_time": issues.actual_date_time,
                    "issues_evaluate_finish": issues.issues_evaluate_finish, "voluntary_apply": issues.voluntary_apply,
                    "issues_evaluate_count": issues.issues_evaluate_count,
                       }
                issues_tables.append(tmp)

        return issues_tables
