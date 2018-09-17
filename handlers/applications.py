#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from orm.issues_info import IssuesInfoModule
from methods.toolkits import DateToolKits
import json
from methods.debug import *
from handlers.decorator import handles_get_auth
from handlers.decorator import handles_post_auth


#继承 base.py 中的类 BaseHandler
class ApplicationsHandler(BaseHandler):
    """
    用户议题申报处理
    """
    @handles_get_auth("/applications")
    def get(self):
        user_name = self.get_current_user()
        # 先判断是否完善其他信息，如果没有完善，跳转到信息完善页面
        if user_name is not None:
            user_topic = self.__get_all_current_user_topics(user_name)
            self.render("applications.html",
                        controller=self.render_controller,
                        user_name=user_name,
                        user_topic=user_topic,
                        )

    @handles_post_auth
    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        response["data"] = date_kits.get_now_day_str()

        operation = self.get_argument("operation")
        topic_name = self.get_argument("topic_name")
        topic_brief = self.get_argument("topic_brief")
        topic_date = self.get_argument("topic_date")
        user_name = self.get_current_user()

        if operation == "apply_issues":
            ret = self.__add_topics(user_name, topic_name, topic_brief, topic_date)
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

    def __get_all_current_user_topics(self, user_name):
        user_tpoic = []
        topics_module = IssuesInfoModule.get_all_issues_info()
        if topics_module is None:
            return user_tpoic

        for topics in topics_module:
            if topics.user_name == user_name:
                tmp = {
                    "topic_id": topics.id, "name": topics.user_name, "image": topics.image, "title": topics.title,
                    "current": topics.current, "finish": topics.finish,  "time": topics.datetime,
                    "description": topics.brief
                       }
                user_tpoic.append(tmp)

        return user_tpoic

    def __add_topics(self, topic_user, topic_name, topic_brief, topic_date):
        rule = self.db.query(IssuesInfoModule).filter(IssuesInfoModule.title == topic_name).first()
        if rule is not None:
            logging.error("current topics is exit")
            return False

        topic_module = IssuesInfoModule()
        topic_module.user_name = topic_user
        topic_module.nick_name = "unknown"
        topic_module.title = topic_name
        topic_module.brief = topic_brief
        topic_module.datetime = topic_date
        topic_module.current = False
        topic_module.finish = False
        topic_module.image = "null"

        self.db.add(topic_module)
        self.db.commit()
        return True
