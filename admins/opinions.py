#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth
from orm.feedback import FeedBackModule


#  继承 base.py 中的类 BaseHandler

class AdminOpinionsHandler(BaseHandler):
    """
    该类只提供跳转到管理页面
    """
    @admin_get_auth("/admin/opinions", False)
    def get(self):
        # 用户渲染表格模板的数据接口
        # 后续该接口需要从数据库读取
        user_name = self.get_current_user()
        if user_name is not None:
            opinions_tables = self.__get_all_opinions_tables()
            self.render("admin/opinions.html",
                        user_name=user_name,
                        controller=self.render_controller,
                        language_mapping=self.language_mapping,
                        opinions_tables=opinions_tables)

    @admin_post_auth(False)
    def post(self):
        pass

    def __get_all_opinions_tables(self):
        opinions_tables = []
        opinion_modules = self.db.query(FeedBackModule).all()
        if opinion_modules is not None:
            for opinion in opinion_modules:
                tmp = {"feedback_id": opinion.id, "serial_number": opinion.serial_number,
                       "issues_title": opinion.issues_title, "issues_details": opinion.issues_details,
                       "report_date": opinion.report_date, "resolved_date": opinion.resolved_date,
                       "solution_methods": opinion.solution_methods, "feedback_status": opinion.status,
                       "report_user_name": opinion.report_user_name, "resolved_user_name": opinion.resolved_user_name
                       }
                opinions_tables.append(tmp)

        return opinions_tables
