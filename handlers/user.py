#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
import json
from methods.debug import *
from orm.user import UserModule
from handlers.decorator import handles_get_auth
from handlers.decorator import handles_post_auth


class UserHandler(BaseHandler):
    @handles_get_auth("/user")
    def get(self):
        self.render_controller["index"] = True

        try:
            username = self.get_argument("user")
        except:
            username = self.get_current_user()
            logging.info("get username from except")
        else:
            logging.info("get username from request")

        next_name = self.get_argument("next", "/login")

        if username is not None:

            self.render("user.html", controller=self.render_controller, username=username, next=next_name)

    @handles_post_auth
    def post(self):
        ret = {"status": True, "data": "", "error": ""}
        username = self.get_argument("username")
        email = self.get_argument("email")
        nickname = self.get_argument("nickname")
        department = self.get_argument("department")
        print("username:%s email:%s nickname:%s department：%s" % (username, email, nickname, department))
        succeed = self.__set_user_info_by_username(username, email, nickname, department)

        if succeed is True:
            logging.info("update user[%s] info succeed." % username)
            self.write(json.dumps(ret))
        else:
            logging.info("update user[%s] info failed." % username)
            ret["status"] = False
            ret["error"] = "更新用户信息失败！"
            self.write(json.dumps(ret))

    def __set_user_info_by_username(self, username, email, nickname, department):
        if email is not None and nickname is not None and department is not None:
            self.db.query(UserModule).filter(UserModule.username == username).update({
                UserModule.email: email,
                UserModule.nickname: nickname,
                UserModule.department: department,
            })
            self.db.commit()
            return True
        else:
            return False
