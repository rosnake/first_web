#!/usr/bin/env Python
# coding=utf-8

import json
from handlers.base import BaseHandler
from methods.toolkits import DateToolKits
from orm.user import UserModule
from methods.debug import *
from handlers.decorator import handles_get_auth
from handlers.decorator import handles_post_auth


class ModifyPassWordHandler(BaseHandler):  # 继承 base.py 中的类 BaseHandler
    @handles_get_auth("/modify_password")
    def get(self):
        username = self.get_current_user()

        # 先判断是否完善其他信息，如果没有完善，跳转到信息完善页面
        if username is not None:
            self.render("modify_password.html", controller=self.render_controller)

    @handles_post_auth
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
