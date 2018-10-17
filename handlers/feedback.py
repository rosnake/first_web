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
            self.render("feedback.html",
                        controller=self.render_controller,
                        user_name=user_name,
                        language_mapping=self.language_mapping,
                        )

    @handles_post_auth
    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        operation = self.get_argument("operation")
        feedback_title = self.get_argument("feedback_title")
        feedback_details = self.get_argument("feedback_details", "none")

        logging.info("operation:%s , feedback_title: %s, feedback_details:%s" % (operation, feedback_title, feedback_details))

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
