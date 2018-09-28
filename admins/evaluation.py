#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from methods.toolkits import DateToolKits
from methods.debug import *
from orm.meeting_info import MeetingInfoModule
from orm.issues_info import IssuesInfoModule
import json
from orm.users_info import UsersInfoModule
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth


# 继承 base.py 中的类 BaseHandler
class AdminEvaluatingHandler(BaseHandler):
    """
    用于评分管理
    """
    @admin_get_auth("/admin/evaluating", False)
    def get(self):
        user_name = self.get_current_user()
        if user_name is not None:
            user_issues_tables = self.__get_all_issues_info()
            self.render("admin/evaluation.html",
                        controller=self.render_controller,
                        user_name=user_name,
                        language_mapping=self.language_mapping,
                        user_issues_tables=user_issues_tables,
                        )

    @admin_post_auth(False)
    def post(self):
        pass

    def __get_all_issues_info(self):
        issues_module = IssuesInfoModule.get_all_issues_info()
        if issues_module is None:
            return None

        issues_tables = []
        for issues in issues_module:
            tmp = {
                "issues_id": issues.id, "keynote_user_name": issues.user_name, "issues_image": issues.issues_image,
                "issues_title": issues.issues_title, "keynote_chinese_name": issues.chinese_name,
                "current": issues.current, "finish": issues.finish,  "date_time": issues.date_time,
                "issues_brief": issues.issues_brief, "issues_score": issues.issues_score,
                "issues_meeting_room": issues.issues_meeting_room,
                "issues_evaluate_finish": issues.issues_evaluate_finish, "voluntary_apply": issues.voluntary_apply
                   }
            issues_tables.append(tmp)

        return issues_tables
