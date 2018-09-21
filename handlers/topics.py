#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from orm.issues_info import IssuesInfoModule
from handlers.decorator import handles_get_auth
from handlers.decorator import handles_post_auth


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
        pass

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
