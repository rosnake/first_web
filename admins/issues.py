#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth


# 继承 base.py 中的类 BaseHandler

class AdminIssuesHandler(BaseHandler):
    """
    用于议题管理的弹窗界面
    """
    @admin_get_auth("/admin/issues", False)
    def get(self):
        user_name = self.get_current_user()
        if user_name is not None:
            self.render("admin/issues.html", controller=self.render_controller)

    @admin_post_auth(False)
    def post(self):
        pass
