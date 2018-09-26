#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from orm.issues_info import IssuesInfoModule
from handlers.decorator import handles_get_auth
from handlers.decorator import handles_post_auth
from methods.toolkits import DateToolKits
from methods.debug import *
import json


# 继承 base.py 中的类 BaseHandler
class TopicsHandler(BaseHandler):
    """
    用户议题显示处理
    """
    @handles_get_auth("/topics")
    def get(self):
        user_name = self.get_current_user()

        if user_name is not None:
            user_topic_tables = self.__get_all_issues_info()
            self.render("topics.html",
                        controller=self.render_controller,
                        user_name=user_name,
                        topics_table=user_topic_tables,
                        language_mapping=self.language_mapping,
                        )

    @handles_post_auth
    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        response["data"] = date_kits.get_now_day_str()

        operation = self.get_argument("operation")
        issues_id = self.get_argument("issues_id")
        prepare_score = self.get_argument("prepare_score")
        novel_score = self.get_argument("novel_score")
        report_score = self.get_argument("report_score")

        logging.info("operation:%s, issues_id:%s,prepare_score:%s,novel_score:%s,report_score:%s"
                     % (operation, issues_id, prepare_score, novel_score,report_score))

        # 需要根据具体情况定
        response["status"] = True
        response["message"] = "评价成功！"
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
