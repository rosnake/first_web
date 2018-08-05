#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from base import BaseHandler
import json
import methods.debug as dbg
import sys
from  methods.utils import UserDataUtils
from  methods.utils import UserAuthUtils
import io  # 导入io模块
from methods.verify import VerifyImage# 导入验证码图片生成插件

class LoginHandler(BaseHandler):    #继承 base.py 中的类 BaseHandler
    def get(self):
        usernames = mrd.select_columns(table="users",column="username")
        one_user = usernames[0][0]
        #print ("one user name:%s" % one_user)
        controller = UserDataUtils.get_render_controller()
        controller["index"] = False
        controller["authorized"] = False
        controller["login"] = True

        self.render("login.html", controller=controller)

    def post(self):    
        ret = {"status":True,"data":"","error":"succeed"}
        username = self.get_argument("username")
        password = self.get_argument("password")
        code = self.get_argument("verify_code")
        vcode = code.upper()
        verify_code = UserAuthUtils.get_verify_code()
        print("username:%s password:%s verify_code_dest:%s, verify_code_src %s" %(username, password, verify_code, vcode))
        if vcode != verify_code:
            dbg.debug_msg(LoginHandler,sys._getframe().f_lineno, "验证码错误处理")
            #self.render("error.html",user=username, controller=controller)
            ret["status"] = False
            ret["error"] = "验证码错误！"
            self.write(json.dumps(ret))
            return

        auth_flags = UserAuthUtils.authenticate_user_by_name(username, password)
        if(auth_flags):
            dbg.debug_msg(LoginHandler,sys._getframe().f_lineno, "redirect home page")
            self.set_current_user(username)
            #self.render("home.html")
            self.write(json.dumps(ret))
        else:
            controller = UserDataUtils.get_render_controller()
            controller["index"] = False
            controller["authorized"] = False
            controller["login"] = True

            dbg.debug_msg(LoginHandler,sys._getframe().f_lineno, "密码错误处理")
            #self.render("error.html",user=username, controller=controller)
            ret["status"] = False
            ret["error"] = "密码错误！"
            self.write(json.dumps(ret))

class VerifyHandler(BaseHandler):
    def get(self):
        #生成图片并且返回
        mstream = io.BytesIO()                          #创建一个BytesIO临时保存生成图片数据
        verify = VerifyImage()
        img = verify.get_image()
        code = verify.get_code()
        UserAuthUtils.set_verify_code(code)
        img.save(mstream,"PNG")                         #将返回的验证码图片数据，添加到BytesIO临时保存
        self.write(mstream.getvalue())                  #从BytesIO临时保存，获取图片返回给img的 src= 进行显示