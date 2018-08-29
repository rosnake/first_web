#!/usr/bin/env Python
# coding=utf-8

import tornado.web
import tornado.escape
import methods.readdb as mrd
from handlers.base import BaseHandler
from  methods.utils import UserDataUtils
import json
import sys
import methods.debug as dbg
from methods.debug import *


class UserHandler(BaseHandler):
    def get(self):
        controller = UserDataUtils.get_render_controller()
        controller["index"] = True
        controller["authorized"] = False
        
        try:
            username = self.get_argument("user")
        except:
            username = self.get_current_user()
            logging.info("get username from except")
        else:
            logging.info("get username from request")

        if username is not None:
            user_infos = mrd.select_table(table="users",column="*",condition="username",value=username)
            self.render("user.html", users = user_infos, controller=controller, username=username)

    def post(self):
        ret = {"status": True, "data": "", "error": ""}
        dbg.debug_msg(UserHandler, sys._getframe().f_lineno, "post register")
        username = self.get_argument("username")
        email = self.get_argument("email")
        nickname = self.get_argument("nickname")
        department = self.get_argument("department")
        print("username:%s email:%s nickname:%s department：%s" % (username, email, nickname, department))


        # print(")
        succeed = True
        if (succeed):
            dbg.debug_msg(UserHandler, sys._getframe().f_lineno, "redirect home page")
            self.write(json.dumps(ret))
        else:
            dbg.debug_msg(UserHandler, sys._getframe().f_lineno, "redirect error page")
            # self.render("register_error.html", user=username)

            ret["status"] = False
            ret["error"] = "用户名已存在！"
            self.write(json.dumps(ret))

