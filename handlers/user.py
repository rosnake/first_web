#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
import json
from methods.debug import *
from orm.users_info import UsersInfoModule
from handlers.decorator import handles_get_auth
from handlers.decorator import handles_post_auth


class UserHandler(BaseHandler):
    @handles_get_auth("/user")
    def get(self):
        self.render_controller["index"] = True

        try:
            user_name = self.get_argument("user")
        except:
            user_name = self.get_current_user()
            logging.info("get user_name from except")
        else:
            logging.info("get user_name from request")

        next_name = self.get_argument("next", "/login")

        if user_name is not None:

            self.render("user.html", controller=self.render_controller, user_name=user_name, next=next_name)

    @handles_post_auth
    def post(self):
        ret = {"status": True, "data": "", "error": ""}
        user_name = self.get_argument("user_name")
        email = self.get_argument("email")
        chinese_name = self.get_argument("chinese_name")
        department = self.get_argument("department")
        print("user_name:%s email:%s chinese_name:%s department：%s" % (user_name, email, chinese_name, department))
        succeed = self.__set_user_info_by_user_name(user_name, email, chinese_name, department)

        if succeed is True:
            logging.info("update user[%s] info succeed." % user_name)
            self.write(json.dumps(ret))
        else:
            logging.info("update user[%s] info failed." % user_name)
            ret["status"] = False
            ret["error"] = "更新用户信息失败！"
            self.write(json.dumps(ret))

    def __set_user_info_by_user_name(self, user_name, email, chinese_name, department):
        if email is not None and chinese_name is not None and department is not None:
            self.db.query(UsersInfoModule).filter(UsersInfoModule.user_name == user_name).update({
                UsersInfoModule.email: email,
                UsersInfoModule.chinese_name: chinese_name,
                UsersInfoModule.department: department,
            })
            self.db.commit()
            return True
        else:
            return False
