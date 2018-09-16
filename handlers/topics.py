#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from orm.topics import TopicsModule
from handlers.decorator import handles_get_auth
from handlers.decorator import handles_post_auth


# 继承 base.py 中的类 BaseHandler
class TopicsHandler(BaseHandler):
    """
    用户议题显示处理
    """
    @handles_get_auth("/topics")
    def get(self):
        username = self.get_current_user()

        if username is not None:
            user_topic_tables = self.__get_all_topics()
            self.render("topics.html",
                        controller=self.render_controller,
                        username=username,
                        topics_table=user_topic_tables,
                        )

    @handles_post_auth
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
