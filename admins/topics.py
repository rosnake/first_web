#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
import json
from methods.toolkits import DateToolKits
from orm.topics import TopicsModule
from methods.debug import *
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth


# 继承 base.py 中的类 BaseHandler
class AdminTopicsHandler(BaseHandler):
    """
    用户话题管理
    """
    @admin_get_auth("/admin/topics", False)
    def get(self):
        username = self.get_current_user()
        if username is not None:
            user_topic_tables = self.__get_all_topics()
            self.render("admin/topics.html",
                        controller=self.render_controller,
                        username=username,
                        user_topic_tables=user_topic_tables,
                        )

    @admin_post_auth(False)
    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        response["data"] = date_kits.get_now_day_str()

        operation = self.get_argument("operation")
        topic_user = self.get_argument("topic_user")
        topic_name = self.get_argument("topic_name")
        topic_brief = self.get_argument("topic_brief")
        topic_date = self.get_argument("topic_date")
        topic_id = self.get_argument("topic_id")

        if operation == "add":
            ret = self.__add_topics(topic_user, topic_name, topic_brief, topic_date)
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

        if operation == "delete":
            ret = self.__delete_topic_by_id(topic_id)
            if ret is True:
                response["status"] = True
                response["message"] = "删除成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "当前积分规则不支持"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

        if operation == "modify":
            ret = self.__modify_topic_by_id(topic_id, topic_user, topic_name, topic_brief, topic_date)
            if ret is True:
                response["status"] = True
                response["message"] = "修改成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "当前议题已存在"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

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

    def __modify_topic_by_id(self, topic_id, topic_user, topic_name, topic_brief, topic_date):
        topic = self.db.query(TopicsModule).filter(TopicsModule.id == topic_id).first()

        if topic is not None:
            self.db.query(TopicsModule).filter(TopicsModule.id == topic_id).update({
                TopicsModule.username: topic_user,
                TopicsModule.title: topic_name,
                TopicsModule.brief: topic_brief,
                TopicsModule.datetime: topic_date,
                })

            self.db.commit()
            logging.info("modify topic succeed")
            return True
        else:
            logging.error("modify topic failed")
            return False

    def __delete_topic_by_id(self, topic_id):
        topic = self.db.query(TopicsModule).filter(TopicsModule.id == topic_id).first()

        if topic is not None:
            self.db.delete(topic)
            self.db.commit()
            logging.info("delete topic succeed")
            return True
        else:
            logging.error("delete topic failed")
            return False