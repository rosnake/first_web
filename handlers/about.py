#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from handlers.base import BaseHandler
from methods.utils import UserDataUtils


# 继承 base.py 中的类 BaseHandler
class AboutHandler(BaseHandler):
    """
    关于页面处理，显示一些客户不需要登陆也可查看的信息
    """
    def get(self):
        usernames = mrd.select_columns(table="users",column="username")
        one_user = usernames[0][0]
        #print ("one user name:%s" % one_user)
        username = self.get_current_user()
        controller = UserDataUtils.get_render_controller()
        controller["index"] = True
        controller["authorized"] = False
        controller["login"] = False
        controller["admin"] = False
        if username is not None:
            controller["authorized"] = True
            print("################"+username)

        persons = UserDataUtils.get_user_info_tables()
        self.render("about.html",
                    controller=controller,
                    username=username,
                    )
