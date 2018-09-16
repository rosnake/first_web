#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from methods.toolkits import DateToolKits
from methods.debug import *
from orm.meeting import MeetingModule
from orm.topics import TopicsModule
import json
from orm.user import UserModule
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth


# 继承 base.py 中的类 BaseHandler
class AdminMeetingHandler(BaseHandler):
    """
    用于会议信息管理
    """
    @admin_get_auth("/admin/meeting", False)
    def get(self):
        username = self.get_current_user()
        if username is not None:
            meeting_tables = self.__get_meeting_table()
            topics_tables = self.__get_all_no_finish_topics()
            self.render("admin/meeting.html",
                        meeting_tables=meeting_tables,
                        controller=self.render_controller,
                        topics_tables=topics_tables,
                        username=username,
                        )

    @admin_post_auth(False)
    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()

        operation = self.get_argument("operation")
        topic_id = self.get_argument("topic_id")
        user_name = self.get_argument("user_name")
        meeting_room = self.get_argument("meeting_room")
        meeting_date = self.get_argument("meeting_date")
        topic_title = self.get_argument("topic_title")
        logging.info("topic_id: "+topic_id)
        if operation == "modify":
            ret = self.__modify_meeting_info_by_topic_id(topic_id, meeting_room, meeting_date)
            if ret is True:
                response["status"] = True
                response["message"] = "修改成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
            else:
                response["status"] = False
                response["message"] = "修改失败！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))

            return

        if operation == "add":
            ret = self.__add_meeting_info(topic_id, user_name, meeting_room, meeting_date, topic_title)
            if ret is True:
                response["status"] = True
                response["message"] = "修改成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
            else:
                response["status"] = False
                response["message"] = "修改失败！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))

            return
        if operation == "set_current":
            ret = self.__set_meeting_to_current(topic_id)
            if ret is True:
                response["status"] = True
                response["message"] = "修改成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
            else:
                response["status"] = False
                response["message"] = "修改失败！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))

            return


    def __get_meeting_table(self):
        meeting_modules = MeetingModule.get_all_meeting()
        meeting_table = []

        if meeting_modules:
            for x in meeting_modules:
                tmp = {"meeting_id": x.id, "topic_id": x.topic_id, "topic_title": x.topic_title,
                       "current_meeting": x.current_meeting, "user_name": x.user_name,
                       "meeting_room": x.meeting_room, "meeting_date": x.meeting_date}

                meeting_table.append(tmp)

        return meeting_table

    def __get_all_no_finish_topics(self):
        topics_module = TopicsModule.get_all_topics()
        if topics_module is None:
            return None

        topics_tables = []
        for topics in topics_module:
            if topics.finish is False:
                tmp = {
                    "topic_id": topics.id, "name": topics.username, "image": topics.image, "title": topics.title,
                    "current": topics.current, "finish": topics.finish,  "time": topics.datetime,
                    "description": topics.brief
                       }
                topics_tables.append(tmp)

        return topics_tables

    def __add_meeting_info(self, topic_id, user_name, meeting_room, meeting_date, topic_title):
        meeting = self.db.query(MeetingModule).filter(MeetingModule.topic_id == topic_id).first()
        if meeting is not None:
            return False

        user = self.db.query(UserModule).filter(UserModule.username == user_name).first()
        if user is not None:
            nickname = user.nickname
        else:
            nickname = "unknown"
        meeting_info = MeetingModule()

        meeting_info.user_name = user_name
        meeting_info.topic_id = topic_id
        meeting_info.nick_name = nickname
        meeting_info.meeting_room = meeting_room
        meeting_info.meeting_date = meeting_date
        meeting_info.current_meeting = False
        meeting_info.topic_title = topic_title

        self.db.add(meeting_info)
        self.db.commit()

        return True

    def __modify_meeting_info_by_topic_id(self, topic_id, meeting_room, meeting_date):
        meeting = self.db.query(MeetingModule).filter(MeetingModule.topic_id == topic_id).first()
        if meeting is None:
            return False

        self.db.query(MeetingModule).filter(MeetingModule.topic_id == topic_id).update({
            MeetingModule.meeting_room: meeting_room,
            MeetingModule.meeting_date: meeting_date,
        })

        self.db.commit()

        return True

    def __set_meeting_to_current(self, topic_id):
        meeting = self.db.query(MeetingModule).filter(MeetingModule.topic_id == topic_id).first()
        if meeting is None:
            return False

        self.db.query(MeetingModule).filter(MeetingModule.topic_id == topic_id).update({
            MeetingModule.current_meeting: True,
        })

        self.db.commit()

        return True
