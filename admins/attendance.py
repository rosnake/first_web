#!/usr/bin/env Python
# coding=utf-8

import json
from handlers.base import BaseHandler
from methods.debug import *
from methods.toolkits import DateToolKits
from orm.attendance import AttendanceModule
from orm.score_info import ScoreInfoModule
from orm.score_criteria import ScoringCriteriaModule
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth


# 继承 base.py 中的类 BaseHandler
class AdminAttendanceHandler(BaseHandler):
    """
    该页面用户出勤相关管理
    """

    @admin_get_auth("/admin/attendance", False)
    def get(self):
        user_name = self.get_current_user()
        if user_name is not None:
            attendance_tables = self.__get_attendance_tables()
            leave_reason = self.__get_all_leave_reason()

            self.render("admin/attendance.html",
                        attendance_tables=attendance_tables,
                        controller=self.render_controller,
                        user_name=user_name,
                        leave_reason=leave_reason,
                        language_mapping=self.language_mapping,
                        )

    @admin_post_auth(False)
    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        operation = self.get_argument("operation")
        user_name = self.get_argument("user_name", "unknown")
        absent_id = self.get_argument("absent_id", -1)

        logging.info("operation:%s , user_name: %s" % (operation, user_name))

        if operation == "leave_accept":
            ret = self.__set_attendance_leave_accept_by_user_name(user_name)
            if ret is True:
                response["status"] = True
                response["message"] = "处理成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "签到失败"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

        if operation == "leave_reject":
            ret = self.__set_attendance_leave_reject_by_user_name(user_name)
            if ret is True:
                response["status"] = True
                response["message"] = "处理成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "签到失败"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

        if operation == "sign":
            ret = self.__attendance_sign_by_user_name(user_name)
            if ret is True:
                response["status"] = True
                response["message"] = "处理成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "签到失败"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

        if operation == "absent":
            ret = self.__set_attendance_absent_by_user_name(user_name, absent_id)
            if ret is True:
                response["status"] = True
                response["message"] = "处理成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "签到失败"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

        if operation == "start_sign":
            ret = self.__start_attendance_sign()
            if ret is True:
                response["status"] = True
                response["message"] = "处理成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "签到失败"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

        if operation == "reset_sign_table":
            ret = self.__reset_attendance_sign_tables()
            if ret is True:
                response["status"] = True
                response["message"] = "复位签到表成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "复位签到表失败"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

        response["status"] = False
        response["message"] = "找不到对应的操作！"
        response["data"] = date_kits.get_now_day_str()
        self.write(json.dumps(response))

        return

    def __get_all_leave_reason(self):
        score_module = ScoringCriteriaModule.get_all_scoring_criteria()

        leave_reason = []
        if score_module:
            for x in score_module:
                if x.score_value < 0:
                    tmp = {"reason_id": x.id, "leave_reason": x.criteria_name}
                    leave_reason.append(tmp)

            return leave_reason
        else:
            return leave_reason

    def __set_attendance_absent_by_user_name(self, user_name, absent_id):
        attendance = self.db.query(AttendanceModule).filter(AttendanceModule.user_name == user_name).first()

        if attendance is not None:
            score_criteria = self.db.query(ScoringCriteriaModule).filter(ScoringCriteriaModule.id == absent_id).first()
            #  更新积分表
            user_point = self.db.query(ScoreInfoModule).filter(ScoreInfoModule.user_name == user_name).first()

            if user_point and score_criteria:
                self.db.query(ScoreInfoModule).filter(ScoreInfoModule.user_name == user_name).update({
                    ScoreInfoModule.last_scores: user_point.current_scores,
                    ScoreInfoModule.current_scores: user_point.current_scores + score_criteria.score_value,
                })
                self.db.commit()
            else:
                return False

            self.db.query(AttendanceModule).filter(AttendanceModule.user_name == user_name).update({
                AttendanceModule.checked_in: True,
                AttendanceModule.attended: True,
                AttendanceModule.absence_apply_accept: True,

            })
            self.db.commit()
            logging.info("modify attendance succeed")
            return True
        else:
            logging.error("modify attendance failed")
            return False

    def __attendance_sign_by_user_name(self, user_name):
        attendance = self.db.query(AttendanceModule).filter(AttendanceModule.user_name == user_name).first()
        date_kits = DateToolKits()

        if attendance is not None:
            self.db.query(AttendanceModule).filter(AttendanceModule.user_name == user_name).update({
                AttendanceModule.checked_in: True,
                AttendanceModule.attended: True,
                AttendanceModule.absence_apply_accept: False,
                AttendanceModule.checked_in_time: date_kits.get_now_str()
            })
            self.db.commit()
            logging.info("modify attendance succeed")
            return True
        else:
            logging.error("modify attendance failed")
            return False

    def __set_attendance_leave_accept_by_user_name(self, user_name):
        attendance = self.db.query(AttendanceModule).filter(AttendanceModule.user_name == user_name).first()

        if attendance is not None:
            score_criteria = self.db.query(ScoringCriteriaModule).filter(ScoringCriteriaModule.id == attendance.absence_id).first()
            #  更新积分表
            user_score = self.db.query(ScoreInfoModule).filter(ScoreInfoModule.user_name == user_name).first()

            if user_score and score_criteria:
                self.db.query(ScoreInfoModule).filter(ScoreInfoModule.user_name == user_name).update({
                    ScoreInfoModule.last_scores: user_score.current_scores,
                    ScoreInfoModule.current_scores: user_score.current_scores + score_criteria.score_value,
                })
                self.db.commit()
            else:
                return False

            date_kits = DateToolKits()
            self.db.query(AttendanceModule).filter(AttendanceModule.user_name == user_name).update({
                AttendanceModule.checked_in: True,
                AttendanceModule.attended: True,
                AttendanceModule.absence_apply_accept: True,
                AttendanceModule.checked_in_time: date_kits.get_now_str(),
            })
            self.db.commit()
            logging.info("modify attendance succeed")
            return True
        else:
            logging.error("modify attendance failed")
            return False

    def __set_attendance_leave_reject_by_user_name(self, user_name):
        attendance = self.db.query(AttendanceModule).filter(AttendanceModule.user_name == user_name).first()

        if attendance is not None:
            self.db.query(AttendanceModule).filter(AttendanceModule.user_name == user_name).update({
                AttendanceModule.checked_in: False,
                AttendanceModule.attended: True,
                AttendanceModule.absence_apply_accept: False,
            })
            self.db.commit()
            logging.info("modify attendance succeed")
            return True
        else:
            logging.error("modify attendance failed")
            return False

    def __get_attendance_tables(self):
        attendance_tables = []

        attendance_modules = AttendanceModule.get_all_attendance_info()

        if attendance_modules:
            for x in attendance_modules:
                if x.user_name != "admin":
                    tmp = {
                        "attendance_id": id, "user_name": x.user_name, "chinese_name": x.chinese_name,
                        "checked_in": x.checked_in, "absence_reason": x.absence_reason, "absence_id": x.absence_id,
                        "attended": x.attended, "absence_apply_time": x.absence_apply_time, "datetime": x.date_time,
                        "absence_apply_accept": x.absence_apply_accept, "checked_in_time": x.checked_in_time,
                    }
                    attendance_tables.append(tmp)

        return attendance_tables

    def __start_attendance_sign(self):
        attendance_modules = AttendanceModule.get_all_attendance_info()

        if attendance_modules is None:
            logging.error("attendance is none")
            return False

        for attendance in attendance_modules:
            if attendance.current_attendance is False:
                logging.info("current change %s attendance status" % attendance.user_name)
                self.db.query(AttendanceModule).filter(AttendanceModule.user_name == attendance.user_name).update({
                    AttendanceModule.checked_in: False,
                    AttendanceModule.attended: True,
                    AttendanceModule.absence_apply_accept: False,
                    AttendanceModule.current_attendance: True,
                })
                self.db.commit()

        return True

    def __reset_attendance_sign_tables(self):
        attendance_modules = AttendanceModule.get_all_attendance_info()

        if attendance_modules is None:
            logging.error("attendance is none")
            return False

        for attendance in attendance_modules:
            self.db.query(AttendanceModule).filter(AttendanceModule.user_name == attendance.user_name).update({
                AttendanceModule.checked_in: False,
                AttendanceModule.attended: True,
                AttendanceModule.absence_apply_accept: False,
                AttendanceModule.current_attendance: True,
            })
            self.db.commit()

        return True

