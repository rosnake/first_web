#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
from handlers.base import BaseHandler
from  methods.utils import UserDataUtils
from  methods.utils import UserAuthUtils
from methods.controller import PageController
from orm.topics import TopicsModule
from methods.toolkits import DateToolKits
import json
from methods.debug import *


#继承 base.py 中的类 BaseHandler
class ApplicationsHandler(BaseHandler):
    """
    用户议题申报处理
    """
    @tornado.web.authenticated
    def get(self):
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()
        if self.session["authorized"] is None or self.session["authorized"] is False:
            self.redirect("/login?next=/applications")
            return

        username = self.get_current_user()

        print(self.session["authorized"])
        render_controller["index"] = False
        render_controller["authorized"] = self.session["authorized"]
        render_controller["login"] = False
        render_controller["admin"] = self.session["admin"]
        render_controller["organizer"] = self.session["organizer"]

        # 先判断是否完善其他信息，如果没有完善，跳转到信息完善页面
        if username is not None:

            user_topic = self.__get_all_current_user_topics(username)
            self.render("applications.html",
                        controller=render_controller,
                        username=username,
                        user_topic=user_topic,
                        )

    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        response["data"] = date_kits.get_now_day_str()

        operation = self.get_argument("operation")
        topic_name = self.get_argument("topic_name")
        topic_brief = self.get_argument("topic_brief")
        topic_date = self.get_argument("topic_date")
        username = self.get_current_user()

        if operation == "apply_issues":
            ret = self.__add_topics(username, topic_name, topic_brief, topic_date)
            if ret is True:
                response["status"] = True
                response["message"] = "新增成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "当前议题已存在"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

    def __get_all_current_user_topics(self, username):
        user_tpoic = []
        topics_module = TopicsModule.get_all_topics()
        if topics_module is None:
            return user_tpoic

        for topics in topics_module:
            if topics.username == username:
                tmp = {
                    "topic_id": topics.id, "name": topics.username, "image": topics.image, "title": topics.title,
                    "current": topics.current, "finish": topics.finish,  "time": topics.datetime,
                    "description": topics.brief
                       }
                user_tpoic.append(tmp)

        return user_tpoic

    def __add_topics(self, topic_user, topic_name, topic_brief, topic_date):
        rule = self.db.query(TopicsModule).filter(TopicsModule.title == topic_name).first()
        if rule is not None:
            logging.error("current topics is exit")
            return False

        topic_module = TopicsModule()
        topic_module.username = topic_user
        topic_module.nickname = "unknown"
        topic_module.title = topic_name
        topic_module.brief = topic_brief
        topic_module.datetime = topic_date
        topic_module.current = False
        topic_module.finish = False
        topic_module.image = "null"

        self.db.add(topic_module)
        self.db.commit()
        return True
