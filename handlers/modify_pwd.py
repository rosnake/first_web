#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.debug as dbg
import json
import sys
from handlers.base import BaseHandler
from methods.controller import PageController
from methods.toolkits import DateToolKits
from orm.user import UserModule
from methods.debug import *


class ModifyPassWordHandler(BaseHandler):  # 继承 base.py 中的类 BaseHandler
    def get(self):
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()
        if self.session["authorized"] is None or self.session["authorized"] is False:
            self.redirect("/login?next=/modify_password")
            return

        username = self.get_current_user()

        print(self.session["authorized"])
        render_controller["index"] = False
        render_controller["authorized"] = self.session["authorized"]
        render_controller["login"] = False
        render_controller["admin"] = self.session["admin"]
        render_controller["organizer"] = self.session["organizer"]

        # 先判断是否完善其他信息，如果没有完善，跳转到信息完善页面
        if username is not None:
            self.render("modify_password.html", controller=render_controller)

    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        username = self.get_argument("username")
        old_password = self.get_argument("old_password")
        new_password = self.get_argument("new_password")
        confirm = self.get_argument("confirm")
        print("username:%s old_password:%s new_password:%s confirm:%s" % (username, old_password, new_password, confirm))
        if new_password != confirm:
            response["status"] = False
            response["message"] = "两次输入的密码不一致！"
            response["data"] = date_kits.get_now_day_str()
            self.write(json.dumps(response))
            return

        if new_password == old_password:
            response["status"] = False
            response["message"] = "新密码不能等于老密码！"
            response["data"] = date_kits.get_now_day_str()
            self.write(json.dumps(response))
            return

        ret = self.__modify_passwd_by_username(username, old_password, new_password)
        if ret is True:
            response["status"] = True
            response["message"] = "修改密码成功！"
            response["data"] = date_kits.get_now_day_str()
            self.write(json.dumps(response))
        else:
            response["status"] = False
            response["message"] = "修改密码失败！"
            response["data"] = date_kits.get_now_day_str()
            self.write(json.dumps(response))

        return

    def __modify_passwd_by_username(self, username, old_password, password):
        user = self.db.query(UserModule).filter(UserModule.username == username).first()

        if user is not None:
            if user.password != old_password:
                logging.error("modify user failed")
                return False

            self.db.query(UserModule).filter(UserModule.username == username).update({
                UserModule.password: password,
                UserModule.pwd_modified: True,
            })

            self.db.commit()
            logging.info("modify user succeed")
            return True
        else:
            logging.error("modify user failed")
            return False
