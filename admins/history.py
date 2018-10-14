#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth
from orm.operation_history import OperationHistoryModule


# 继承 base.py 中的类 BaseHandler

class AdminHistoryHandler(BaseHandler):
    """
    用于议题管理的弹窗界面
    """
    @admin_get_auth("/admin/history", False)
    def get(self):
        user_name = self.get_current_user()
        history_info = self.__get_all_history_info()

        if user_name is not None:
            self.render("admin/history.html", controller=self.render_controller,
                        language_mapping=self.language_mapping,
                        history_info=history_info,
                        user_name=user_name,
                        )

    @admin_post_auth(False)
    def post(self):
        pass

    def __get_all_history_info(self):
        history_info = []

        history_module = OperationHistoryModule.get_all_history_info()
        if history_module:
            for history in history_module:
                tmp = {"operation_user_name": history.operation_user_name, "operation_time": history.operation_time,
                       "impact_user_name": history.impact_user_name, "operation_details": history.operation_details,
                       "id": history.id,
                       }
                history_info.append(tmp)

        return history_info
