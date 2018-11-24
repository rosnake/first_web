#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from methods.toolkits import DateToolKits
from methods.debug import *
from orm.score_history import ScoringHistoryModule
from orm.issues_info import IssuesInfoModule
from orm.score_info import ScoreInfoModule
import json
from orm.evaluation_info import EvaluationInfoModule
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth
from orm.score_criteria import ScoringCriteriaModule
from orm.operation_history import OperationHistoryModule


# 继承 base.py 中的类 BaseHandler
class AdminEvaluatingHandler(BaseHandler):
    """
    用于评分管理
    """
    @admin_get_auth("/admin/evaluating", False)
    def get(self):
        user_name = self.get_current_user()
        if user_name is not None:
            user_issues_tables = self.__get_all_issues_info()
            self.render("admin/evaluation.html",
                        controller=self.render_controller,
                        user_name=user_name,
                        language_mapping=self.language_mapping,
                        user_issues_tables=user_issues_tables,
                        )

    @admin_post_auth(False)
    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        response["data"] = date_kits.get_now_day_str()

        operation = self.get_argument("operation")
        issues_id = self.get_argument("issues_id")
        logging.info("operation:"+operation+" issues_id:"+issues_id)

        if operation == "evaluate_finish":
            ret = self.__finish_issues_evaluation(issues_id)
            if ret is True:
                response["status"] = True
                response["message"] = "结束评价成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "结束评价失败"
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
                "issues_meeting_room": issues.issues_meeting_room,
                "issues_evaluate_finish": issues.issues_evaluate_finish, "voluntary_apply": issues.voluntary_apply
                   }
            issues_tables.append(tmp)

        return issues_tables

    def __finish_issues_evaluation(self, issues_id):
        issues = self.db.query(IssuesInfoModule).filter(IssuesInfoModule.id == issues_id).first()
        if issues is None:
            return False

        # 1、计算议题得分
        evaluation_module = self.db.query(EvaluationInfoModule).filter(
            EvaluationInfoModule.issues_id == issues_id).filter(EvaluationInfoModule.evaluate_finish == False).all()
        if evaluation_module is None:
            return False

        date_time = DateToolKits().get_now_time()
        issues_prepare_score = 0
        issues_content_score = 0
        issues_lecture_score = 0
        evaluation_count = 0

        for evaluation in evaluation_module:
            logging.info("====》evaluation_count:%d" % evaluation_count)
            evaluation_count = evaluation_count + 1
            issues_prepare_score = issues_prepare_score + evaluation.issues_prepare_score
            issues_content_score = issues_content_score + evaluation.issues_content_score
            issues_lecture_score = issues_lecture_score + evaluation.issues_lecture_score

            self.db.query(EvaluationInfoModule).filter(EvaluationInfoModule.id == evaluation.id).update({
                EvaluationInfoModule.evaluate_finish: True,
                EvaluationInfoModule.date_time: date_time,
            })
            self.db.commit()

        logging.info("evaluation_count:%d" % evaluation_count)

        if evaluation_count is not 0:
            issues_prepare_score = issues_prepare_score / evaluation_count
            issues_content_score = issues_content_score / evaluation_count
            issues_lecture_score = issues_lecture_score / evaluation_count
        else:
            return False

        logging.info("issues_prepare_score:%d, issues_content_score:%d, issues_lecture_score:%d"
                     % (issues_prepare_score, issues_content_score, issues_lecture_score))
        last_score = (issues_prepare_score + issues_content_score + issues_lecture_score) / 3
        logging.info("last_score:%d, evaluation_count:%d" % (last_score, evaluation_count))

        # 2、将议题标记为结束
        self.db.query(IssuesInfoModule).filter(IssuesInfoModule.id == issues_id).update({
            IssuesInfoModule.issues_evaluate_finish: True,
            IssuesInfoModule.issues_score: last_score,

        })
        self.db.commit()

        # 3、更新用户得分信息
        real_score = last_score
        #  3.1 是否是系统用户
        if issues.is_system_user is True:
            #  3.2 是否是主动申请
            if issues.voluntary_apply is True:
                score_rule = self.db.query(ScoringCriteriaModule).\
                    filter(ScoringCriteriaModule.criteria_name == "主动申报").first()
                if score_rule:
                    real_score = last_score + score_rule.score_value
                    logging.info("current issues is apply, add %d" % score_rule.score_value)
                    history_module = ScoringHistoryModule()
                    history_module.user_name = issues.user_name
                    history_module.criteria_id = score_rule.id
                    history_module.criteria_name = score_rule.criteria_name
                    history_module.score_value = score_rule.score_value  # 对应分数
                    history_module.transactor = self.get_current_user()  # 处理人
                    history_module.date_time = date_time  # 处理时间
                    self.db.add(history_module)
                    self.db.commit()
                    opt = "add issues apply score"
                    self.record_operation_history(issues.user_name, opt)

            user_point = self.db.query(ScoreInfoModule).filter(ScoreInfoModule.user_name == issues.user_name).first()

            if user_point:
                self.db.query(ScoreInfoModule).filter(ScoreInfoModule.user_name == issues.user_name).update({
                    ScoreInfoModule.last_scores: user_point.current_scores,
                    ScoreInfoModule.current_scores: user_point.current_scores + real_score,
                })
                self.db.commit()
                logging.info("update user score Succeed")
            else:
                logging.info("update user score failed")

            # 4、更新用户得分历史信息
            score_rule = self.db.query(ScoringCriteriaModule).filter(ScoringCriteriaModule.criteria_name == "议题得分") \
                .first()
            if score_rule:
                history_module = ScoringHistoryModule()
                history_module.user_name = issues.user_name
                history_module.criteria_id = score_rule.id
                history_module.criteria_name = score_rule.criteria_name
                history_module.score_value = last_score  # 对应分数
                history_module.transactor = self.get_current_user()  # 处理人
                history_module.date_time = date_time  # 处理时间
                self.db.add(history_module)
                self.db.commit()

                opt = "add issues score"
                self.record_operation_history(issues.user_name, opt)

        return True

