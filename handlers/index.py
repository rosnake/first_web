#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from methods.controller import PageController
from orm.issues_info import IssuesInfoModule
from orm.meeting_info import MeetingInfoModule
from methods.debug import *

# 继承 base.py 中的类 BaseHandler
class IndexHandler(BaseHandler):
    """
    用户首页处理，显示一些客户不需要登陆也可查看的信息
    """
    def get(self):
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()

        render_controller["index"] = True
        render_controller["login"] = False

        if self.session["authorized"] is None:
            render_controller["authorized"] = False
            render_controller["admin"] = False
            render_controller["organizer"] = False
        else:
            render_controller["authorized"] = self.session["authorized"]
            render_controller["admin"] = self.session["admin"]
            render_controller["organizer"] = self.session["organizer"]

        user_name = self.get_current_user()
        topics_table = self.__get_all_topic_tables()
        current_meeting = self.__get_current_meeting_info()
        self.render("handlers/index.html",
                    topics_table=topics_table,
                    controller=render_controller,
                    current_meeting=current_meeting,
                    user_name=user_name,
                    language_mapping=self.language_mapping,
                    )

    def post(self):
        pass

    def __get_all_topic_tables(self):
        topics_module = IssuesInfoModule.get_all_issues_info()
        if topics_module is None:
            return None

        topics_tables = []
        for topics in topics_module:
            tmp = {
                "topic_id": topics.id, "name": topics.user_name, "image": topics.issues_image, "title": topics.issues_title,
                "current": topics.current, "finish": topics.finish, "time": topics.expect_date_time,
                "description": topics.issues_brief
            }
            topics_tables.append(tmp)

        return topics_tables

    def __get_current_meeting_info(self):
        all_meeting = MeetingInfoModule.get_all_meeting_info()
        if all_meeting:
            for x in all_meeting:
                if x.current_meeting is True:
                    current_meeting = {
                        "meeting_id": x.id, "user_name": x.keynote_user_name, "chinese_name": x.keynote_chinese_name,
                        "meeting_room": x.meeting_room, "topic_title": x.issues_title,
                        "meeting_date": x.meeting_date, "current_meeting": x.current_meeting
                    }
                    return current_meeting

            return None
        else:
            return None

