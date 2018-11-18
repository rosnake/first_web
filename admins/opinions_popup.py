#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from methods.debug import *
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth
from orm.feedback import FeedBackModule
from methods.toolkits import DateToolKits
import json
# 继承 base.py 中的类 BaseHandler


class AdminOpinionsPopupHandler(BaseHandler):
    """
    该类用于话题修改弹窗处理
    """

    @admin_get_auth("/admin/opinions_popup", False)
    def get(self):
        # 用户渲染表格模板的数据接口
        # 后续该接口需要从数据库读取
        serial_number = self.get_argument("serial_number", "none")
        status = self.get_argument("status", "closed")

        page_button_hide = False
        if status == "closed":
            page_button_hide = True
        # 无效编号，回到主界面
        if serial_number == "none":
            self.redirect("/admin/opinions")
            return

        logging.info("[opinions_popup]:serial_number:"+serial_number)
        user_name = self.get_current_user()
        if user_name is not None:
            opinions = self.__get_opinions_by_id(serial_number)
            if opinions is not None:
                self.render("admin/opinions_popup.html",
                            controller=self.render_controller,
                            opinions=opinions,
                            language_mapping=self.language_mapping,
                            page_button_hide=page_button_hide,
                            )

    @admin_post_auth(False)
    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()

        operation = self.get_argument("operation")
        serial_number = self.get_argument("serial_number")
        resolved_status = self.get_argument("resolved_status")
        solution_methods = self.get_argument("solution_methods")

        if operation == "resolved":
            ret = self.__update_opinions_by_serial_number(serial_number, resolved_status,solution_methods)
            if ret is True:
                response["status"] = True
                response["message"] = "更新问题状态失败"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
            else:
                response["status"] = False
                response["message"] = "更新问题状态成功"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

    def __update_opinions_by_serial_number(self, serial_number, status, solution):
        opinions = self.db.query(FeedBackModule).filter(FeedBackModule.serial_number == serial_number).first()
        if opinions is None:
            return False

        date = DateToolKits()

        self.db.query(FeedBackModule).filter(FeedBackModule.serial_number == serial_number).update({
            FeedBackModule.status: status,
            FeedBackModule.solution_methods: solution,
            FeedBackModule.resolved_date: date.get_now_day_str(),
            FeedBackModule.resolved_user_name: self.get_current_user()
        })
        self.db.commit()
        logging.info("update feedback status ok")
        return True

    def __get_opinions_by_id(self, serial_number):
        opinion = self.db.query(FeedBackModule).filter(FeedBackModule.serial_number == serial_number).first()

        if opinion is not None:
            opinions = {"feedback_id": opinion.id, "serial_number": opinion.serial_number,
                        "issues_title": opinion.issues_title, "issues_details": opinion.issues_details,
                        "report_date": opinion.report_date, "resolved_date": opinion.resolved_date,
                        "solution_methods": opinion.solution_methods, "feedback_status": opinion.status,
                        "report_user_name": opinion.report_user_name, "resolved_user_name": opinion.resolved_user_name
                        }

            return opinions
        else:
            return None
