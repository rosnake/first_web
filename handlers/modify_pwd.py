#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.debug as dbg
import json
import sys
from handlers.base import BaseHandler
from methods.utils import UserDataUtils


class ModifyPassWordHandler(BaseHandler):  # 继承 base.py 中的类 BaseHandler
    def get(self):
        dbg.debug_msg(ModifyPassWordHandler, sys._getframe().f_lineno, "get modify password")
        controller = UserDataUtils.get_render_controller()
        controller["index"] = False
        controller["authorized"] = True
        controller["login"] = False
        self.render("modify_password.html", controller=controller)

    def post(self):
        ret = {"status": True, "data": "", "error": ""}
        dbg.debug_msg(ModifyPassWordHandler, sys._getframe().f_lineno, "post modify password")
        username = self.get_argument("username")
        old_password = self.get_argument("old_password")
        new_password = self.get_argument("new_password")
        confirm = self.get_argument("confirm")
        print("username:%s old_password:%s new_password:%s confirm:%s" % (username, old_password,new_password, confirm))
        # print(")
        succeed = False
        if (succeed):
            dbg.debug_msg(ModifyPassWordHandler, sys._getframe().f_lineno, "redirect home page")
            # self.render("home.html")
            self.write(json.dumps(ret))
            # self.redirect("home.html")

        else:
            dbg.debug_msg(ModifyPassWordHandler, sys._getframe().f_lineno, "redirect error page")
            # self.render("register_error.html", user=username)

            ret["status"] = False
            ret["error"] = "用户名已存在！"
            self.write(json.dumps(ret))
