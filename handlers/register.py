#!/usr/bin/env Python
# coding=utf-8

from methods.debug import *
import json
from handlers.base import BaseHandler
from orm.users_info import UsersInfoModule
from orm.score_info import ScoreInfoModule
from methods.controller import PageController
from orm.attendance import AttendanceModule
from orm.operation_history import OperationHistoryModule
from config.default_config import DefaultScoreConfig


#  继承 base.py 中的类 BaseHandler
class RegisterHandler(BaseHandler):
    def get(self):
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()

        logging.info(self.session["authorized"])
        render_controller["index"] = False
        render_controller["authorized"] = False
        render_controller["login"] = True
        render_controller["admin"] = False
        render_controller["organizer"] = False

        self.render("handlers/register.html", controller=render_controller,
                    language_mapping=self.language_mapping,
                    )
        
    def post(self):
        ret = {"status": True, "data": "", "message": ""}
        user_name = self.get_argument("user_name")
        password = self.get_argument("password")
        confirm = self.get_argument("confirm")
        print("user_name:%s password:%s confirm:%s" % (user_name, password, confirm))
        # 先查询用户是否存在
        user = self.db.query(UsersInfoModule).filter(UsersInfoModule.user_name == user_name).first()
        succeed = False
        # 不存在创建用户
        if user is None:
            user_module = UsersInfoModule()
            user_module.user_name = user_name
            user_module.pass_word = password
            user_module.chinese_name = "unknown"
            user_module.address = "unknown"
            user_module.department = "unknown"
            user_module.email = "unknown"
            user_module.user_role = "normal"
            user_module.nick_name = "unknown"
            user_module.pwd_modified = True
            user_module.change_pwd_count = 0
            self.db.add(user_module)
            self.db.commit()

            # 更新积分表格
            scores_module = ScoreInfoModule()
            scores_module.user_name = user_name
            scores_module.current_scores = DefaultScoreConfig.current_scores
            scores_module.last_scores = DefaultScoreConfig.last_scores
            scores_module.chinese_name = user_module.chinese_name
            scores_module.purchase_points = False

            self.db.add(scores_module)
            self.db.commit()
            succeed = True

            attendance = AttendanceModule()
            attendance.user_name = user_name
            attendance.chinese_name = user_module.chinese_name
            attendance.absence_reason = "unknown"
            attendance.absence_id = 0
            attendance.attended = True
            attendance.checked_in = True
            attendance.absence_apply_accept = True

            self.db.add(attendance)
            self.db.commit()

            # 更新session信息
            self.set_current_user(user_name)
            self.session["authorized"] = True
            self.session["user_name"] = user_name
            self.session["admin"] = False
            self.session["organizer"] = False

            # 记录操作历史
            history = OperationHistoryModule()
            history.operation_user_name = user_name
            history.operation_details = "register a new user"
            history.impact_user_name = user_name

            self.db.add(history)
            self.db.commit()

        if succeed is True:
            self.write(json.dumps(ret))
        else:
            ret["status"] = False
            ret["error"] = "用户名已存在！"
            self.write(json.dumps(ret))
