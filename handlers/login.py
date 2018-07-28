#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from base import BaseHandler
import json
import methods.debug as dbg
import sys

class LoginHandler(BaseHandler):    #继承 base.py 中的类 BaseHandler
    def get(self):
        usernames = mrd.select_columns(table="users",column="username")
        one_user = usernames[0][0]
        #print ("one user name:%s" % one_user)
        self.render("login.html")

    def post(self):    
        ret = {"status":True,"data":"","error":"succeed"}
        username = self.get_argument("username")
        password = self.get_argument("password")
        
        print("username:%s password:%s " %(username, password))
        
        succeed = True
        if(succeed):
            dbg.debug_msg(LoginHandler,sys._getframe().f_lineno, "redirect home page")
            #self.render("home.html")
            self.write(json.dumps(ret))
        else:
            dbg.debug_msg(LoginHandler,sys._getframe().f_lineno, "错误处理")
            #self.render("home.html")
            ret["status"] = False
            ret["error"] = "密码错误！"
            self.write(json.dumps(ret))
