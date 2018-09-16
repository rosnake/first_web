#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from methods.controller import PageController
from orm.topics import TopicsModule
from orm.meeting import MeetingModule


# 继承 base.py 中的类 BaseHandler
class IndexHandler(BaseHandler):
    """
    用户首页处理，显示一些客户不需要登陆也可查看的信息
    """
    def get(self):
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()

        render_controller["index"] = True
        render_controller["authorized"] = self.session["authorized"]
        render_controller["login"] = False
        render_controller["admin"] = self.session["admin"]
        render_controller["organizer"] = self.session["organizer"]

        username = self.get_current_user()
        topics_table = self.__get_all_topic_tables()
        current_meeting = self.__get_current_meeting_info()
        self.render("index.html",
                    topics_table=topics_table,
                    controller=render_controller,
                    current_meeting=current_meeting,
                    username=username,
                    )

    def post(self):
        pass

    def __get_all_topic_tables(self):
        topics_module = TopicsModule.get_all_topics()
        if topics_module is None:
            return None

        topics_tables = []
        for topics in topics_module:
            tmp = {
                "topic_id": topics.id, "name": topics.username, "image": topics.image, "title": topics.title,
                "current": topics.current, "finish": topics.finish, "time": topics.datetime,
                "description": topics.brief
            }
            topics_tables.append(tmp)

        return topics_tables

    def __get_current_meeting_info(self):
        all_meeting = MeetingModule.get_all_meeting()
        if all_meeting:
            for x in all_meeting:
                if x.current_meeting is True:
                    current_meeting = {
                        "meeting_id": x.id, "user_name": x.user_name, "nick_name": x.nick_name,
                        "meeting_room": x.meeting_room, "topic_title": x.topic_title,
                        "meeting_date": x.meeting_date, "current_meeting": x.current_meeting
                    }
                    return current_meeting

            return None
        else:
            return None

