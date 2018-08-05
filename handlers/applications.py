#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from base import BaseHandler
from  methods.utils import UserDataUtils
#继承 base.py 中的类 BaseHandler
class ApplicationsHandler(BaseHandler):
    """
    用户议题申报处理
    """
    def get(self):
         #print ("one user name:%s" % one_user)
        username=self.get_current_user()
        controller = UserDataUtils.get_render_controller()
        controller["index"] = False
        controller["authorized"] = False
        controller["login"] = False

        user_topic = UserDataUtils.get_user_topics_by_name(username)

        if username != None:
            controller["authorized"] = True
            print("################"+username)

        self.render("applications.html",
                    controller =controller,
                    username=username,
                    user_topic=user_topic,
                    )

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        user_infos = mrd.select_table(table="users",column="*",condition="username",value=username)
        if user_infos:
            db_pwd = user_infos[0][2]
            if db_pwd == password:
                print("username:%s pwd:%s db_pwd %s" % (username, password, db_pwd))
                self.set_current_user(username)    #将当前用户名写入 cookie，方法见下面
                self.write(username)
            else:
                print("username:%s pwd:%s " % (username, password))
                self.write("-1")
        else:
            self.write("-1")
