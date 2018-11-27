#!/usr/bin/env Python
# coding=utf-8

import json
from handlers.base import BaseHandler
from methods.debug import *
from orm.users_info import UsersInfoModule
from orm.score_info import ScoreInfoModule
from methods.toolkits import DateToolKits
from orm.score_criteria import ScoringCriteriaModule
from orm.attendance import AttendanceModule
from handlers.decorator import handles_get_auth
from handlers.decorator import handles_post_auth
from orm.meeting_info import MeetingInfoModule


# 继承 base.py 中的类 BaseHandler

class HomeHandler(BaseHandler):
    """
    该类处理的主要是登陆后显示的主页和基于主页的操作
    该类只有在登陆成功后才会显示主页页面，登陆失败，不显示该页面
    """

    @handles_get_auth("/home")
    def get(self):
        user_name = self.get_current_user()

        # 先判断是否完善其他信息，如果没有完善，跳转到信息完善页面
        if user_name is not None:
            user = self.db.query(UsersInfoModule).filter(UsersInfoModule.user_name == user_name).first()
            if user is not None:
                logging.info("current user is :%s" % user.user_name)
                if user.email == "unknown":
                    self.redirect("/user?next=/home")
                    self.finish()
                    return

        points_table = self.__get_all_point_tables()
        current_meeting_flags, meeting_info = self.__get_current_meeting_info()
        self.render("handlers/home.html", points_table=points_table, controller=self.render_controller,
                    user_name=user_name,
                    language_mapping=self.language_mapping,
                    current_meeting_flags=current_meeting_flags,
                    meeting_info=meeting_info,
                    )

    @handles_post_auth
    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        operation = self.get_argument("operation")
        user_name = self.get_argument("user_name")
        leave_id = self.get_argument("leave_id", 0)
        leave_date = self.get_argument("leave_date", "none")

        logging.info("operation:%s , user_name: %s, leave_id:%s leave_date: %s" % (operation, user_name, leave_id, leave_date))

        if operation == "absent_apply":
            logging.info(leave_date)
            time_diff = date_kits.cac_time_diff_with_current_by_str(leave_date)
            logging.info("time diff:" + str(time_diff))
            valid_time = date_kits.check_time_is_ok(leave_date)

            if valid_time is False:
                response["status"] = False
                response["message"] = "选择时间不能早已当前时间！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                logging.info("time out of range")
                return

            ret = self.__leave_apply_by_id(user_name, leave_id, leave_date)

            if ret is True:
                response["status"] = True
                response["message"] = "申请成功！"
                response["data"] = date_kits.get_now_day_str()
                opt = "apply a absent, username: " + user_name
                self.record_operation_history(user_name, opt)
                self.write(json.dumps(response))
            else:
                response["status"] = False
                response["message"] = "申请失败！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))

            return

    def __leave_apply_by_id(self, user_name, leave_id, leave_date):
        criteria = self.db.query(ScoringCriteriaModule).filter(ScoringCriteriaModule.id == leave_id).first()
        if criteria is None:
            logging.error("not scoring criteria exist, leave_id = %s" % leave_id)
            return False
        attendance = self.db.query(AttendanceModule).filter(AttendanceModule.user_name == user_name).first()

        if attendance is None:
            logging.error("not attendance exist user_name=%s" % user_name)
            return False

        date_kits = DateToolKits()
        absence_apply_time = date_kits.get_now_time()  # 申请时间

        self.db.query(AttendanceModule).filter(AttendanceModule.user_name == user_name).update({
            AttendanceModule.absence_reason: criteria.criteria_name,
            AttendanceModule.absence_id: criteria.id,
            AttendanceModule.attended: False,
            AttendanceModule.absence_apply_accept: False,
            AttendanceModule.absence_apply_time: absence_apply_time,
            AttendanceModule.date_time: leave_date,
        })

        self.db.commit()
        logging.info("user leave apply  succeed")

        return True

    def __get_all_point_tables(self):
        points_tables = []

        point_module = ScoreInfoModule.get_all_score_info()

        if point_module is None:
            return points_tables

        for point in point_module:
            tmp = {
                "user_name": point.user_name, "chinese_name": point.chinese_name,
                "current_scores": point.current_scores, "last_scores": point.last_scores
            }
            points_tables.append(tmp)

        return points_tables

    def __get_current_meeting_info(self):
        meeting_info = []
        current_meeting_flags = False
        meeting = self.db.query(MeetingInfoModule).filter(MeetingInfoModule.current_meeting == True).all()
        if meeting:
            for x in meeting:
                logging.info("current meeting id:%d, issues_title:%s" % (x.id, x.issues_title))
                tmp = {"meeting_id": x.id, "issues_title": x.issues_title, "keynote_user_name": x.keynote_user_name,
                       "meeting_room": x.meeting_room, "meeting_date": x.meeting_date,
                       "keynote_chinese_name": x.keynote_chinese_name
                       }
                meeting_info.append(tmp)
            current_meeting_flags = True
        return current_meeting_flags, meeting_info

