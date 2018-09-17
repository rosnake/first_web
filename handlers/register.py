#!/usr/bin/env Python
# coding=utf-8

from methods.debug import *
import json
import sys
from handlers.base import BaseHandler
from orm.users_info import UsersInfoModule
from orm.score_info import ScoreInfoModule
from methods.controller import PageController

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

        self.render("register.html",controller=render_controller)
        
    def post(self):
        ret = {"status": True, "data": "", "message": ""}
        user_name = self.get_argument("user_name")
        password = self.get_argument("password")
        confirm = self.get_argument("confirm")
        print("user_name:%s password:%s confirm:%s" % (user_name, password, confirm))
        # 先查询用户是否存在
        user = self.db.query(UsersInfoModule).filter(UsersInfoModule.user_name == user_name).first()
        print(user)
        succeed = False
        # 不存在创建用户
        if user is None:
            user_moudle = UsersInfoModule()
            user_moudle.user_name = user_name
            user_moudle.password = password
            user_moudle.nick_name = "unknown"
            user_moudle.address = "unknown"
            user_moudle.department = "unknown"
            user_moudle.email = "unknown"
            user_moudle.user_role = "normal"
            user_moudle.pwd_modified = True
            self.db.add(user_moudle)
            self.db.commit()
            # 更新积分表格
            point_moudle = ScoreInfoModule()
            point_moudle.user_name = user_name
            point_moudle.current_point = 10
            point_moudle.last_point = 10
            point_moudle.nick_name = user_moudle.nick_name
            self.db.add(point_moudle)
            self.db.commit()
            succeed = True

        if succeed is True:
            self.write(json.dumps(ret))
        else:
            ret["status"] = False
            ret["error"] = "用户名已存在！"
            self.write(json.dumps(ret))
