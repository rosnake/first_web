#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from base import BaseHandler
import json
import methods.debug as dbg
import sys


class LayerHandler(BaseHandler):
    """
    该类主要用户处理弹出页面以及弹出页面相关操作。
    1、根据用户提供的信息在数据库查询后显示相应的编辑窗口
    2、根据用户编辑后的提交信息，写如数据库，并返回相关状态
    """
    def get(self):
        user = "hello world"
        user = self.get_argument("user")
        print("====username:"+user)
        self.render("layer.html", username=user)

    def post(self):
        ret = {"status": True, "data": "", "error": "succeed"}
        username = self.get_argument("username")
        password = self.get_argument("password")

        print("username:%s password:%s " % (username, password))

        succeed = True
        if (succeed):
            dbg.debug_msg(LoginHandler, sys._getframe().f_lineno, "redirect home page")
            # self.render("home.html")
            self.write(json.dumps(ret))
        else:
            dbg.debug_msg(LoginHandler, sys._getframe().f_lineno, "错误处理")
            # self.render("home.html")
            ret["status"] = False
            ret["error"] = "密码错误！"
            self.write(json.dumps(ret))
