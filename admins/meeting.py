#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from methods.toolkits import DateToolKits
from methods.debug import *
from orm.meeting_info import MeetingInfoModule
from orm.issues_info import IssuesInfoModule
from orm.attendance import AttendanceModule
import json
from orm.users_info import UsersInfoModule
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth


# 继承 base.py 中的类 BaseHandler
class AdminMeetingHandler(BaseHandler):
    """
    用于会议信息管理
    """
    @admin_get_auth("/admin/meeting", False)
    def get(self):
        user_name = self.get_current_user()
        if user_name is not None:
            meeting_tables = self.__get_meeting_table()
            topics_tables = self.__get_all_no_finish_topics()
            self.render("admin/meeting.html",
                        meeting_tables=meeting_tables,
                        controller=self.render_controller,
                        topics_tables=topics_tables,
                        user_name=user_name,
                        language_mapping=self.language_mapping,
                        )

    @admin_post_auth(False)
    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()

        operation = self.get_argument("operation")
        issues_id = self.get_argument("issues_id")
        keynote_user_name = self.get_argument("keynote_user_name")
        meeting_room = self.get_argument("meeting_room")
        meeting_date = self.get_argument("meeting_date")
        issues_title = self.get_argument("issues_title")
        logging.info("issues_id: "+issues_id)
        if operation == "modify":
            ret = self.__modify_meeting_info_by_issues_id(issues_id, meeting_room, meeting_date)
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
            ret = self.__add_meeting_info(issues_id, keynote_user_name, meeting_room, meeting_date, issues_title)
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

        if operation == "del":
            ret = self.__delete_meeting_info_by_id(issues_id)
            if ret is True:
                response["status"] = True
                response["message"] = "删除当前会议成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
            else:
                response["status"] = False
                response["message"] = "删除当前会议失败！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))

            return

        if operation == "set_current":
            ret = self.__set_meeting_to_current(issues_id)
            if ret is True:
                response["status"] = True
                response["message"] = "设置为当前议题成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
            else:
                response["status"] = False
                response["message"] = "设置当前议题失败！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))

            return

        if operation == "issues_finish":
            ret = self.__finish_current_meeting(issues_id)
            if ret is True:
                response["status"] = True
                response["message"] = "结束当前会议成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
            else:
                response["status"] = False
                response["message"] = "结束当前会议失败！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))

            return

        if operation == "issues_cancel":
            ret = self.__cancel_current_meeting(issues_id)
            if ret is True:
                response["status"] = True
                response["message"] = "取消当前会议成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
            else:
                response["status"] = False
                response["message"] = "取消当前会议失败！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))

            return


    def __get_meeting_table(self):
        meeting_modules = MeetingInfoModule.get_all_meeting_info()
        meeting_table = []

        if meeting_modules:
            for x in meeting_modules:
                tmp = {"meeting_id": x.id, "issues_id": x.issues_id, "issues_title": x.issues_title,
                       "current_meeting": x.current_meeting, "keynote_user_name": x.keynote_user_name,
                       "meeting_room": x.meeting_room, "meeting_date": x.meeting_date,
                       "meeting_finish": x.meeting_finish
                       }

                meeting_table.append(tmp)

        return meeting_table

    def __get_all_no_finish_topics(self):
        issues_module = IssuesInfoModule.get_all_issues_info()
        if issues_module is None:
            return None

        issues_tables = []
        for issues in issues_module:
            if issues.finish is False:
                tmp = {
                    "issues_id": issues.id, "keynote_user_name": issues.user_name,
                    "issues_image": issues.issues_image, "issues_brief": issues.issues_brief,
                    "issues_title": issues.issues_title, "current_issues": issues.current,
                    "issues_finish": issues.finish,  "present_time": issues.date_time,
                    "keynote_chinese_name": issues.chinese_name,
                       }
                issues_tables.append(tmp)

        return issues_tables

    def __add_meeting_info(self, issues_id, keynote_user_name, meeting_room, meeting_date, issues_title):
        meeting = self.db.query(MeetingInfoModule).filter(MeetingInfoModule.issues_id == issues_id).first()
        if meeting is not None:
            return False

        user = self.db.query(UsersInfoModule).filter(UsersInfoModule.user_name == keynote_user_name).first()
        if user is not None:
            chinese_name = user.chinese_name
        else:
            chinese_name = "unknown"
        meeting_info = MeetingInfoModule()

        meeting_info.keynote_user_name = keynote_user_name
        meeting_info.issues_id = issues_id
        meeting_info.keynote_chinese_name = chinese_name
        meeting_info.meeting_room = meeting_room
        meeting_info.meeting_date = meeting_date
        meeting_info.current_meeting = False
        meeting_info.issues_title = issues_title

        self.db.add(meeting_info)
        self.db.commit()

        self.db.query(IssuesInfoModule).filter(IssuesInfoModule.id == issues_id).update({
            IssuesInfoModule.issues_meeting_room: meeting_room,
        })
        self.db.commit()

        return True

    def __modify_meeting_info_by_issues_id(self, issues_id, meeting_room, meeting_date):
        meeting = self.db.query(MeetingInfoModule).filter(MeetingInfoModule.issues_id == issues_id).first()
        if meeting is None:
            return False

        self.db.query(MeetingInfoModule).filter(MeetingInfoModule.issues_id == issues_id).update({
            MeetingInfoModule.meeting_room: meeting_room,
            MeetingInfoModule.meeting_date: meeting_date,
        })

        self.db.commit()

        return True

    def __set_meeting_to_current(self, issues_id):
        meeting = self.db.query(MeetingInfoModule).filter(MeetingInfoModule.issues_id == issues_id).first()
        if meeting is None:
            return False

        issues = self.db.query(IssuesInfoModule).filter(IssuesInfoModule.id == issues_id).first()
        if issues is None:
            return False

        self.db.query(IssuesInfoModule).filter(IssuesInfoModule.id == issues_id).update({
            IssuesInfoModule.current: True,
            IssuesInfoModule.date_time: meeting.meeting_date,
        })
        self.db.commit()

        self.db.query(MeetingInfoModule).filter(MeetingInfoModule.issues_id == issues_id).update({
            MeetingInfoModule.current_meeting: True,
        })

        self.db.commit()

        return True

    def __finish_current_meeting(self, issues_id):
        meeting = self.db.query(MeetingInfoModule).filter(MeetingInfoModule.issues_id == issues_id).first()
        if meeting is None:
            return False

        issues = self.db.query(IssuesInfoModule).filter(IssuesInfoModule.id == issues_id).first()
        if issues is None:
            return False

        self.db.query(IssuesInfoModule).filter(IssuesInfoModule.id == issues_id).update({
            IssuesInfoModule.current: False,
            IssuesInfoModule.issues_evaluate_finish: False,
            IssuesInfoModule.finish: True,

        })
        self.db.commit()

        self.db.query(MeetingInfoModule).filter(MeetingInfoModule.issues_id == issues_id).update({
            MeetingInfoModule.current_meeting: False,
            MeetingInfoModule.meeting_finish: True,

        })
        self.db.commit()

        attendance_modules = AttendanceModule.get_all_attendance_info()
        if attendance_modules is not None:
            for attendance in attendance_modules:
                if attendance.current_attendance is True:
                    self.db.query(AttendanceModule).filter(AttendanceModule.user_name == attendance.user_name).update({
                        AttendanceModule.current_attendance: False,
                    })
                    self.db.commit()

        return True

    def __delete_meeting_info_by_id(self, issues_id):
        logging.info("issues_id:"+issues_id)
        meeting = self.db.query(MeetingInfoModule).filter(MeetingInfoModule.issues_id == issues_id).first()
        if meeting is None:
            return False

        self.db.delete(meeting)
        self.db.commit()

        return True

    def __cancel_current_meeting(self, issues_id):
        meeting = self.db.query(MeetingInfoModule).filter(MeetingInfoModule.issues_id == issues_id).first()
        if meeting is None:
            return False

        issues = self.db.query(IssuesInfoModule).filter(IssuesInfoModule.id == issues_id).first()
        if issues is None:
            return False

        self.db.query(IssuesInfoModule).filter(IssuesInfoModule.id == issues_id).update({
            IssuesInfoModule.current: False,
        })
        self.db.commit()

        self.db.query(MeetingInfoModule).filter(MeetingInfoModule.issues_id == issues_id).update({
            MeetingInfoModule.current_meeting: False,
        })

        self.db.commit()

        return True
