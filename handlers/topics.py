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
            ret = self.__evaluate_by_issues_id( issues_id, prepare_score, novel_score, report_score)
            if ret is True:
                response["status"] = True
                response["message"] = "评价成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "积分兑换失败"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return



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

    def __evaluate_by_issues_id(self, issues_id, prepare_score, novel_score, report_score):
        issues_module = self.db.query(IssuesInfoModule).filter(IssuesInfoModule.id == issues_id).first()

        if issues_module is None:
            return False

        user_name = self.get_current_user()

        if user_name is None:
            return False

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

        return True
