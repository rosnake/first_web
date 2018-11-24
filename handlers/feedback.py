#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from handlers.decorator import handles_get_auth
from handlers.decorator import handles_post_auth
from methods.debug import *
from orm.feedback import FeedBackModule
from methods.toolkits import DateToolKits
import json
import random
import string


# 继承 base.py 中的类 BaseHandler
class FeedBackHandler(BaseHandler):
    """
    关于页面处理，显示关于信息
    """
    @handles_get_auth("/feedback")
    def get(self):
        user_name = self.get_current_user()

        if user_name is not None:
            opinions_tables = self.__get_opinions_tables_by_current_user()
            self.render("handlers/feedback.html",
                        controller=self.render_controller,
                        user_name=user_name,
                        language_mapping=self.language_mapping,
                        opinions_tables=opinions_tables,
                        )

    @handles_post_auth
    def post(self):

        operation = "none"
        feedback_title = "none"
        feedback_details = "none"
        serial_number = "0"

        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        operation = self.get_argument("operation")

        if operation == "feedback":
            feedback_title = self.get_argument("feedback_title", "none")
            feedback_details = self.get_argument("feedback_details", "none")
            logging.info("operation:%s , feedback_title: %s, feedback_details:%s" % (operation, feedback_title,
                                                                                     feedback_details))

        else:
            serial_number = self.get_argument("serial_number", "0")
            logging.info("operation:%s , serial_number:%s" % (operation, serial_number))

        if operation == "feedback":
            ret = self.__feedback_process(feedback_title, feedback_details)
            if ret is True:
                response["status"] = True
                response["message"] = "反馈成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
            else:
                response["status"] = False
                response["message"] = "反馈失败！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))

            return

        if operation == "succeed":
            ret = self.__feedback_regression_succeed_process(serial_number)
            if ret is True:
                response["status"] = True
                response["message"] = "提交成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
            else:
                response["status"] = False
                response["message"] = "提交失败！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))

            return

        if operation == "failure":
            ret = self.__feedback_regression_failure_process(serial_number)
            if ret is True:
                response["status"] = True
                response["message"] = "提交成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
            else:
                response["status"] = False
                response["message"] = "提交失败！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))

            return

    def __feedback_process(self, feedback_title, feedback_details):
        feedback_module = self.db.query(FeedBackModule).filter(FeedBackModule.issues_title == feedback_title).first()
        if feedback_module is not None:
            logging.error("feedback issues is exist")
            return False

        date_kits = DateToolKits()
        random_str = ''.join(random.sample(string.digits, 4))
        serial_number = date_kits.get_now_str() + random_str
        logging.info("serial_number:"+serial_number)

        feedback_module = FeedBackModule()
        feedback_module.serial_number = serial_number
        feedback_module.issues_title = feedback_title
        feedback_module.issues_details = feedback_details
        feedback_module.solution_methods = "unknown"
        feedback_module.report_user_name = self.get_current_user()
        feedback_module.resolved_user_name = "unknown"
        feedback_module.status = "open"

        self.db.add(feedback_module)
        self.db.commit()

        return True

    def __get_opinions_tables_by_current_user(self):
        opinions_tables = []
        current_user = self.get_current_user()

        opinion_modules = self.db.query(FeedBackModule).filter(FeedBackModule.report_user_name == current_user).all()
        if opinion_modules is not None:
            for opinion in opinion_modules:
                tmp = {"feedback_id": opinion.id, "serial_number": opinion.serial_number,
                       "issues_title": opinion.issues_title, "issues_details": opinion.issues_details,
                       "report_date": opinion.report_date, "resolved_date": opinion.resolved_date,
                       "solution_methods": opinion.solution_methods, "feedback_status": opinion.status,
                       "report_user_name": opinion.report_user_name, "resolved_user_name": opinion.resolved_user_name
                       }
                opinions_tables.append(tmp)

        return opinions_tables

    def __feedback_regression_succeed_process(self, serial_number):
        opinion_modules = self.db.query(FeedBackModule).filter(FeedBackModule.serial_number == serial_number).first()
        if opinion_modules is not None:
            self.db.query(FeedBackModule).filter(FeedBackModule.serial_number == serial_number).update({
                FeedBackModule.status: "closed",
            })
            self.db.commit()

            return True
        else:
            return False

    def __feedback_regression_failure_process(self, serial_number):
        opinion_modules = self.db.query(FeedBackModule).filter(FeedBackModule.serial_number == serial_number).first()
        if opinion_modules is not None:
            self.db.query(FeedBackModule).filter(FeedBackModule.serial_number == serial_number).update({
                FeedBackModule.status: "reopen",
            })
            self.db.commit()

            return True
        else:
            return False
