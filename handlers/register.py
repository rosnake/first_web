#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
import methods.debug as dbg
import json
import sys
from base import BaseHandler
from  methods.utils import UserDataUtils

class RegisterHandler(BaseHandler):    #继承 base.py 中的类 BaseHandler
    def get(self):
        dbg.debug_msg(RegisterHandler,sys._getframe().f_lineno, "get register")
        controller = UserDataUtils.get_render_controller()
        controller["index"] = False
        controller["authorized"] = False
        controller["login"] = True
        self.render("register.html",controller=controller)
        
    def post(self):
        ret = {"status":True,"data":"","error":""}
        dbg.debug_msg(RegisterHandler,sys._getframe().f_lineno, "post register")
        username = self.get_argument("username")
        password = self.get_argument("password")
        confirm  = self.get_argument("confirm")
        print("username:%s password:%s confirm:%s" %(username, password, confirm))
        #print(")
        succeed = False
        if(succeed):
            dbg.debug_msg(RegisterHandler,sys._getframe().f_lineno, "redirect home page")
            #self.render("home.html")
            self.write(json.dumps(ret))
            #self.redirect("home.html")
            
        else:
            dbg.debug_msg(RegisterHandler,sys._getframe().f_lineno, "redirect error page")
            #self.render("register_error.html", user=username)
            
            ret["status"] = False
            ret["error"] = "用户名已存在！"
            self.write(json.dumps(ret))
        