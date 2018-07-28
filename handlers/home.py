#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from base import BaseHandler

class HomeHandler(BaseHandler):    #继承 base.py 中的类 BaseHandler
    def get(self):
        usernames = mrd.select_columns(table="users",column="username")
        one_user = usernames[0][0]
        #print ("one user name:%s" % one_user)
        person_li=[["raoyuanqin","-1","0","0","0","10分"], ["chenmeijing","-1","0","0","0","11分"],["raohaha","-1","0","0","0","9分"],["chenhaha","-1","0","0","0","9分"]]
        self.render("home.html", tables=person_li)

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
