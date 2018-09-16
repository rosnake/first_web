#!/usr/bin/env Python
# coding=utf-8

from methods.debug import *
import json
import sys
from handlers.base import BaseHandler
from orm.user import UserModule
from orm.points import PointsModule
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
        username = self.get_argument("username")
        password = self.get_argument("password")
        confirm = self.get_argument("confirm")
        print("username:%s password:%s confirm:%s" % (username, password, confirm))
        # 先查询用户是否存在
        user = self.db.query(UserModule).filter(UserModule.username == username).first()
        print(user)
        succeed = False
        # 不存在创建用户
        if user is None:
            user_moudle = UserModule()
            user_moudle.username = username
            user_moudle.password = password
            user_moudle.nickname = "unknown"
            user_moudle.address = "unknown"
            user_moudle.department = "unknown"
            user_moudle.email = "unknown"
            user_moudle.role = "normal"
            user_moudle.pwd_modified = True
            self.db.add(user_moudle)
            self.db.commit()
            # 更新积分表格
            point_moudle = PointsModule()
            point_moudle.username = username
            point_moudle.current_point = 10
            point_moudle.last_point = 10
            point_moudle.nickname = user_moudle.nickname
            self.db.add(point_moudle)
            self.db.commit()
            succeed = True

        if succeed is True:
            self.write(json.dumps(ret))
        else:
            ret["status"] = False
            ret["error"] = "用户名已存在！"
            self.write(json.dumps(ret))
