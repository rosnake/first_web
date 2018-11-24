#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from orm.issues_info import IssuesInfoModule
from orm.evaluation_info import EvaluationInfoModule
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
                     % (operation, issues_id, prepare_score, novel_score, report_score))

        if operation == "evaluate":
            ret, message = self.__evaluate_by_issues_id(issues_id, prepare_score, novel_score, report_score)
            if ret is True:
                response["status"] = True
                response["message"] = "评价成功！"
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

    def __evaluate_by_issues_id(self, issues_id, prepare_score, novel_score, report_score):
        issues_module = self.db.query(IssuesInfoModule).filter(IssuesInfoModule.id == issues_id).first()

        if issues_module is None:
            return False, "没有待评价议题"

        user_name = self.get_current_user()

        if user_name is None:
            return False, "获取用户失败"

        evaluation = self.db.query(EvaluationInfoModule).filter(EvaluationInfoModule.issues_id == issues_id).\
            filter(EvaluationInfoModule.evaluate_user_name == user_name).first()
        if evaluation:
            self.db.query(EvaluationInfoModule).filter(EvaluationInfoModule.issues_id == issues_id).update({
                EvaluationInfoModule.evaluate_finish: False
            })
            self.db.commit()
            logging.info("already evaluate")
            return False, "您已评价该议题"

        date_kits = DateToolKits()
        evaluation_module = EvaluationInfoModule()
        evaluation_module.issues_id = issues_module.id  # 议题ID
        evaluation_module.issues_title = issues_module.issues_title  # 议题名称
        evaluation_module.keynote_user_name = issues_module.user_name  # 主讲人用户名
        evaluation_module.evaluate_user_name = user_name  # 评价者用户名
        evaluation_module.evaluate_time = date_kits.get_now_time()  # 评价时间

        evaluation_module.issues_prepare_score = prepare_score  # 议题准备情况得分
        evaluation_module.issues_content_score = novel_score  # 议题内容得分
        evaluation_module.issues_lecture_score = report_score  # 演讲情况得分
        evaluation_module.issues_reserved_score = 0  # 保留备用
        evaluation_module.evaluate_finish = False  # 是否结束评价

        self.db.add(evaluation_module)
        self.db.commit()

        logging.info("issues_evaluate_count:%d" % issues_module.issues_evaluate_count)
        self.db.query(IssuesInfoModule).filter(IssuesInfoModule.id == issues_id).update({
            IssuesInfoModule.issues_evaluate_count: issues_module.issues_evaluate_count + 1,
        })
        self.db.commit()

        return True
