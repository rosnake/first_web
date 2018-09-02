#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
import methods.debug as dbg
import json
import sys
from base import BaseHandler
from methods.utils import UserDataUtils
from orm.user import UserModule
from orm.points import PointsModule


class RegisterHandler(BaseHandler):    #继承 base.py 中的类 BaseHandler
    def get(self):
        dbg.debug_msg(RegisterHandler, sys._getframe().f_lineno, "get register")
        controller = UserDataUtils.get_render_controller()
        controller["index"] = False
        controller["authorized"] = False
        controller["login"] = True
        self.render("register.html",controller=controller)
        
    def post(self):
        ret = {"status": True, "data": "", "message": ""}
        dbg.debug_msg(RegisterHandler, sys._getframe().f_lineno, "post register")
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
            dbg.debug_msg(RegisterHandler,sys._getframe().f_lineno, "redirect home page")
            self.write(json.dumps(ret))
        else:
            dbg.debug_msg(RegisterHandler,sys._getframe().f_lineno, "redirect error page")
            ret["status"] = False
            ret["error"] = "用户名已存在！"
            self.write(json.dumps(ret))
