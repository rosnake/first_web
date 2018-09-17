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
            self.render("admin/evaluation.html",
                        controller=self.render_controller,
                        user_name=user_name,
                        )

    @admin_post_auth(False)
    def post(self):
        pass
