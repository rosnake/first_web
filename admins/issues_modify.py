#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
from handlers.base import BaseHandler
from methods.utils import UserDataUtils
from methods.utils import UserAuthUtils
from methods.controller import PageController
from orm.topics import TopicsModule
from methods.debug import *

# 继承 base.py 中的类 BaseHandler


class AdminIssuesModifyHandler(BaseHandler):
    """
    该类处理的主要是登陆后显示的主页和基于主页的操作
    该类只有在登陆成功后才会显示主页页面，登陆失败，不显示该页面
    """
    def get(self):
        # 用户渲染表格模板的数据接口
        # 后续该接口需要从数据库读取
        issues_id = self.get_argument("issues_id")
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()
        if self.session["authorized"] is None or self.session["authorized"] is False:
            self.redirect("/login?next=/admin/topics")
            return

        username = self.get_current_user()
        if username is None:
            self.redirect("/login?next=/admin/topics")
            return

        print(self.session["authorized"])
        render_controller["index"] = False
        render_controller["authorized"] = self.session["authorized"]
        render_controller["login"] = False
        render_controller["admin"] = self.session["admin"]
        render_controller["organizer"] = self.session["organizer"]

        print("issues_id:"+issues_id)
        issues_table = self.__get_topics_by_id(issues_id)
        if issues_table is not None:
            self.render("admin/issues_modify.html", controller=render_controller, issues_table=issues_table)

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
