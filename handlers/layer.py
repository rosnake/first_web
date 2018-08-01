#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from base import BaseHandler
import json
from  methods.debug import debug_msg
import sys
from  methods.utils import  UserDataUtils

class LayerHandler(BaseHandler):
    """
    该类主要用户处理弹出页面以及弹出页面相关操作。
    1、根据用户提供的信息在数据库查询后显示相应的编辑窗口
    2、根据用户编辑后的提交信息，写如数据库，并返回相关状态
    """

    def get(self):
        username = "hello world"
        username = self.get_argument("user")
        operation = self.get_argument("operation")
        debug_msg(LayerHandler, sys._getframe().f_lineno,"====username:"+username)
        debug_msg(LayerHandler, sys._getframe().f_lineno, "====operation:" + operation)
        user_score = UserDataUtils.get_user_score_by_name(username)
        print(user_score)
        if user_score != False:
            debug_msg(LayerHandler, sys._getframe().f_lineno,"render layer.html");
            self.render("layer.html", userscore=user_score)
        else:
            debug_msg(LayerHandler, sys._getframe().f_lineno,"no render layer.html");

    def post(self):
        ret = {"status": True, "data": "", "error": "succeed"}
        username = self.get_argument("username")
        password = self.get_argument("password")

        print("username:%s password:%s " % (username, password))

        succeed = True
        if (succeed):
            debug_msg(LayerHandler, sys._getframe().f_lineno, "redirect home page")
            # self.render("home.html")
            self.write(json.dumps(ret))
        else:
            debug_msg(LayerHandler, sys._getframe().f_lineno, "错误处理")
            # self.render("home.html")
            ret["status"] = False
            ret["error"] = "密码错误！"
            self.write(json.dumps(ret))
