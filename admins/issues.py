#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth
from orm.users_info import UsersInfoModule


# 继承 base.py 中的类 BaseHandler

class AdminIssuesHandler(BaseHandler):
    """
    用于议题管理的弹窗界面
    """
    @admin_get_auth("/admin/issues", False)
    def get(self):
        user_name = self.get_current_user()
        user_info = self.__get_all_user_info()

        if user_name is not None:
            self.render("admin/issues.html", controller=self.render_controller,
                        language_mapping=self.language_mapping,
                        user_info=user_info,
                        )

    @admin_post_auth(False)
    def post(self):
        pass

    def __get_all_user_info(self):
        usr_info = []

        users = UsersInfoModule.get_all_users_info()
        if users:
            for usr in users:
                usr_info.append(usr.user_name)

        return usr_info
