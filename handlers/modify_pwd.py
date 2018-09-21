#!/usr/bin/env Python
# coding=utf-8

import json
from handlers.base import BaseHandler
from methods.toolkits import DateToolKits
from orm.users_info import UsersInfoModule
from methods.debug import *
from handlers.decorator import handles_get_auth
from handlers.decorator import handles_post_auth


class ModifyPassWordHandler(BaseHandler):  # 继承 base.py 中的类 BaseHandler
    @handles_get_auth("/modify_password")
    def get(self):
        user_name = self.get_current_user()

        # 先判断是否完善其他信息，如果没有完善，跳转到信息完善页面
        if user_name is not None:
            self.render("modify_password.html", controller=self.render_controller,
                        language_mapping=self.language_mapping,
                        )

    @handles_post_auth
    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        user_name = self.get_argument("user_name")
        old_pass_word = self.get_argument("old_password")
        new_pass_word = self.get_argument("new_password")
        confirm = self.get_argument("confirm")
        print("user_name:%s old_pass_word:%s new_pass_word:%s confirm:%s" % (user_name, old_pass_word, new_pass_word, confirm))
        if new_pass_word != confirm:
            response["status"] = False
            response["message"] = "两次输入的密码不一致！"
            response["data"] = date_kits.get_now_day_str()
            self.write(json.dumps(response))
            return

        if new_pass_word == old_pass_word:
            response["status"] = False
            response["message"] = "新密码不能等于老密码！"
            response["data"] = date_kits.get_now_day_str()
            self.write(json.dumps(response))
            return

        ret = self.__modify_passwd_by_user_name(user_name, old_pass_word, new_pass_word)
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

    def __modify_passwd_by_user_name(self, user_name, old_pass_word, pass_word):
        user = self.db.query(UsersInfoModule).filter(UsersInfoModule.user_name == user_name).first()

        if user is not None:
            if user.pass_word != old_pass_word:
                logging.error("modify user failed")
                return False

            self.db.query(UsersInfoModule).filter(UsersInfoModule.user_name == user_name).update({
                UsersInfoModule.pass_word: pass_word,
                UsersInfoModule.pwd_modified: True,
            })

            self.db.commit()
            logging.info("modify user succeed")
            return True
        else:
            logging.error("modify user failed")
            return False
