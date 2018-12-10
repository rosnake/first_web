#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from orm.issues_info import IssuesInfoModule
from orm.evaluation_info import EvaluationInfoModule
from handlers.decorator import handles_get_auth
from handlers.decorator import handles_post_auth
from methods.toolkits import DateToolKits
from orm.assessment import AssessmentInfoModule
from methods.debug import *
import json


# 继承 base.py 中的类 BaseHandler
class TopicsAssessmentHandler(BaseHandler):
    """
    用户议题显示处理
    """
    @handles_get_auth("/topics")
    def get(self):
        user_name = self.get_current_user()

        if user_name is not None:
            user_topic_tables = self.__get_all_issues_info()
            self.render("handlers/topic_assessment.html",
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

        logging.info("operation:%s, issues_id:%s"
                     % (operation, issues_id))

        interested = False
        if operation == "interested":
            interested = True
        elif operation == "uninterested":
            interested = False
        else:
            response["status"] = False
            response["message"] = "异常失败！"
            response["data"] = date_kits.get_now_day_str()
            self.write(json.dumps(response))
            return

        user_name = self.get_current_user()
        ret, message = self.__mark_interested_by_issues_id(issues_id, interested, user_name)
        if ret is True:
            response["status"] = True
            response["message"] = "反馈成功！"
            response["data"] = date_kits.get_now_day_str()
            self.write(json.dumps(response))
            return
        else:
            response["status"] = False
            response["message"] = message
            response["data"] = date_kits.get_now_day_str()
            self.write(json.dumps(response))
            return

    def __get_all_issues_info(self):
        issues_module = IssuesInfoModule.get_all_issues_info()
        if issues_module is None:
            return None

        issues_tables = []
        for issues in issues_module:
            tmp = {
                "issues_id": issues.id, "keynote_user_name": issues.user_name, "issues_image": issues.issues_image,
                "issues_title": issues.issues_title, "keynote_chinese_name": issues.chinese_name,
                "current": issues.current, "finish": issues.finish,  "date_time": issues.expect_date_time,
                "issues_brief": issues.issues_brief, "issues_score": issues.issues_score,
                "issues_meeting_room": issues.issues_meeting_room, "actual_date_time": issues.actual_date_time,
                "issues_evaluate_finish": issues.issues_evaluate_finish, "voluntary_apply": issues.voluntary_apply,
                "issues_evaluate_count": issues.issues_evaluate_count,
                   }
            issues_tables.append(tmp)

        return issues_tables

    def __mark_interested_by_issues_id(self, issues_id, interested, user_name):

        issues_module = self.db.query(IssuesInfoModule).filter(IssuesInfoModule.id == issues_id).first()

        if issues_module:
            assessment_module = self.db.query(AssessmentInfoModule).filter(AssessmentInfoModule.issues_id == issues_id).\
                filter(AssessmentInfoModule.assessment_user_name == user_name).first()

            interested_count = issues_module.interested_count
            uninterested_count = issues_module.uninterested_count
            date_kits = DateToolKits()
            #  已存在
            if assessment_module:
                if interested is True:
                    if assessment_module.interested is True:
                        return True, "评估议题成功"
                    else:
                        interested_count = interested_count + 1
                        uninterested_count = uninterested_count - 1
                else:
                    if assessment_module.interested is False:
                        return True, "评估议题成功"
                    else:
                        interested_count = interested_count - 1
                        uninterested_count = uninterested_count + 1

                self.db.query(AssessmentInfoModule).filter(AssessmentInfoModule.issues_id == issues_id).update({
                    AssessmentInfoModule.interested: interested,
                })
                self.db.commit()

                self.db.query(IssuesInfoModule).filter(IssuesInfoModule.id == issues_id).update({
                    IssuesInfoModule.interested_count: interested_count,
                    IssuesInfoModule.uninterested_count: uninterested_count,
                })
                self.db.commit()

                return True, "评估议题成功"
            else:  # 不存在
                assessments = AssessmentInfoModule()
                assessments.issues_id = issues_id  # 议题ID
                assessments.assessment_user_name = user_name  # 评估者
                assessments.assessment_time = date_kits.get_now_time()  # 评估时间
                assessments.assessment_finish = False
                if interested is True:
                    assessments.interested = True
                    interested_count = interested_count + 1
                else:
                    assessments.interested = False
                    uninterested_count = uninterested_count + 1

                self.db.add(assessments)
                self.db.commit()

                self.db.query(IssuesInfoModule).filter(IssuesInfoModule.id == issues_id).update({
                    IssuesInfoModule.interested_count: interested_count,
                    IssuesInfoModule.uninterested_count: uninterested_count,
                })
                self.db.commit()
                return True, "评估议题成功"

        else:
            return False, "没有待评估议题"

