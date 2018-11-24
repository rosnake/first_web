#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from orm.issues_info import IssuesInfoModule
from methods.debug import *
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth

# 继承 base.py 中的类 BaseHandler


class IssuesBrowseHandler(BaseHandler):
    """
    该类用于话题修改弹窗处理
    """
    @admin_get_auth("/browse", False)
    def get(self):
        # 用户渲染表格模板的数据接口
        # 后续该接口需要从数据库读取
        issues_id = self.get_argument("issues_id")
        logging.info("[issues_browse]:issues_id:"+issues_id)
        user_name = self.get_current_user()
        if user_name is not None:
            issues_table = self.__get_issues_info_by_id(issues_id)
            if issues_table is not None:
                self.render("issues_browse.html",
                            controller=self.render_controller,
                            issues_table=issues_table,
                            language_mapping=self.language_mapping,
                            )

    @admin_post_auth(False)
    def post(self):
        pass

    def __get_issues_info_by_id(self, issues_id):

        issues = self.db.query(IssuesInfoModule).filter(IssuesInfoModule.id == issues_id).first()
        if issues:
            issues_item = {
                "issues_id": issues.id, "keynote_user_name": issues.user_name, "issues_image": issues.issues_image,
                "issues_title": issues.issues_title, "keynote_chinese_name": issues.chinese_name,
                "current": issues.current, "finish": issues.finish,  "date_time": issues.expect_date_time,
                "issues_brief": issues.issues_brief, "issues_score": issues.issues_score,
                "issues_meeting_room": issues.issues_meeting_room, "actual_date_time": issues.actual_date_time,
                "issues_evaluate_finish": issues.issues_evaluate_finish, "voluntary_apply": issues.voluntary_apply,
                "issues_evaluate_count": issues.issues_evaluate_count,
                   }

            return issues_item

        else:
            issues_item = {}
            return issues_item


