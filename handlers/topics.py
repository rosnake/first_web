#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
from handlers.base import BaseHandler
from methods.utils import UserDataUtils
from methods.controller import PageController
from orm.topics import TopicsModule


# 继承 base.py 中的类 BaseHandler
class TopicsHandler(BaseHandler):
    """
    用户议题显示处理
    """
    def get(self):
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()
        if self.session["authorized"] is None or self.session["authorized"] is False:
            self.redirect("/login?next=/topics")
            return

        username = self.get_current_user()

        print(self.session["authorized"])
        render_controller["index"] = False
        render_controller["authorized"] = self.session["authorized"]
        render_controller["login"] = False
        render_controller["admin"] = self.session["admin"]
        render_controller["organizer"] = self.session["organizer"]

        if username is not None:
            user_topic_tables = self.__get_all_topics()
            self.render("topics.html",
                        controller=render_controller,
                        username=username,
                        topics_table=user_topic_tables,
                        )

    def post(self):
        pass


    def __get_all_topics(self):
        topics_module = TopicsModule.get_all_topics()
        if topics_module is None:
            return None

        topics_tables = []
        for topics in topics_module:
            tmp = {
                "topic_id": topics.id, "name": topics.username, "image": topics.image, "title": topics.title,
                "current": topics.current, "finish": topics.finish,  "time": topics.datetime,
                "description": topics.brief
                   }
            topics_tables.append(tmp)

        return topics_tables
