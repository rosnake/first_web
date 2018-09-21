#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
import json
from methods.toolkits import DateToolKits
from orm.issues_info import IssuesInfoModule
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
        user_name = self.get_current_user()
        if user_name is not None:
            user_topic_tables = self.__get_all_issues_info()
            self.render("admin/topics.html",
                        controller=self.render_controller,
                        user_name=user_name,
                        user_topic_tables=user_topic_tables,
                        language_mapping=self.language_mapping,
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

    def __get_all_issues_info(self):
        topics_module = IssuesInfoModule.get_all_issues_info()
        if topics_module is None:
            return None

        topics_tables = []
        for topics in topics_module:
            tmp = {
                "topic_id": topics.id, "name": topics.user_name, "image": topics.issues_image, "title": topics.issues_title,
                "current": topics.current, "finish": topics.finish,  "time": topics.date_time,
                "description": topics.issues_brief
                   }
            topics_tables.append(tmp)

        return topics_tables

    def __add_topics(self, topic_user, topic_name, topic_brief, topic_date):
        rule = self.db.query(IssuesInfoModule).filter(IssuesInfoModule.issues_title == topic_name).first()
        if rule is not None:
            logging.error("current topics is exit")
            return False

        topic_module = IssuesInfoModule()
        topic_module.user_name = topic_user
        topic_module.chinese_name = "unknown"
        topic_module.issues_title = topic_name
        topic_module.issues_brief = topic_brief
        topic_module.date_time = topic_date
        topic_module.current = False
        topic_module.finish = False
        topic_module.issues_image = "null"

        self.db.add(topic_module)
        self.db.commit()
        return True

    def __modify_topic_by_id(self, topic_id, topic_user, topic_name, topic_brief, topic_date):
        topic = self.db.query(IssuesInfoModule).filter(IssuesInfoModule.id == topic_id).first()

        if topic is not None:
            self.db.query(IssuesInfoModule).filter(IssuesInfoModule.id == topic_id).update({
                IssuesInfoModule.user_name: topic_user,
                IssuesInfoModule.issues_title: topic_name,
                IssuesInfoModule.issues_brief: topic_brief,
                IssuesInfoModule.date_time: topic_date,
                })

            self.db.commit()
            logging.info("modify topic succeed")
            return True
        else:
            logging.error("modify topic failed")
            return False

    def __delete_topic_by_id(self, topic_id):
        topic = self.db.query(IssuesInfoModule).filter(IssuesInfoModule.id == topic_id).first()

        if topic is not None:
            self.db.delete(topic)
            self.db.commit()
            logging.info("delete topic succeed")
            return True
        else:
            logging.error("delete topic failed")
            return False