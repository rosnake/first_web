#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from orm.topics import TopicsModule
from methods.debug import *
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth

# 继承 base.py 中的类 BaseHandler


class AdminIssuesModifyHandler(BaseHandler):
    """
    该类用于话题修改弹窗处理
    """

    @admin_get_auth("/admin/issues_modify", False)
    def get(self):
        # 用户渲染表格模板的数据接口
        # 后续该接口需要从数据库读取
        issues_id = self.get_argument("issues_id")
        logging.info("[issues_modify]:issues_id:"+issues_id)
        username = self.get_current_user()
        if username is not None:
            issues_table = self.__get_topics_by_id(issues_id)
            if issues_table is not None:
                self.render("admin/issues_modify.html", controller=self.render_controller, issues_table=issues_table)

    @admin_post_auth(False)
    def post(self):
        pass

    def __get_topics_by_id(self, issues_id):
        topics = self.db.query(TopicsModule).filter(TopicsModule.id == issues_id).first()

        if topics is not None:
            tables = {
                "topic_id": topics.id, "name": topics.username, "image": topics.image, "title": topics.title,
                "current": topics.current, "finish": topics.finish, "time": topics.datetime,
                "description": topics.brief
            }

            return tables
        else:
            return None
