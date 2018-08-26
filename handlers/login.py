#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from methods.debug import *
from handlers.base import BaseHandler
import json
import methods.debug as dbg
import sys
from methods.utils import UserDataUtils
from methods.utils import UserAuthUtils
import io  # 导入io模块
from methods.verify import VerifyImage  # 导入验证码图片生成插件
from methods.controller import PageController  # 导入页面控制器
from methods.code import VerifyCode
from methods.toolkits import DateToolKits


# 继承 base.py 中的类 BaseHandler
class LoginHandler(BaseHandler):

    def get(self):
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()
        render_controller["index"] = False
        render_controller["login"] = True
        render_controller["authorized"] = False

        logging.info("get login page")
        self.render("login.html", controller=render_controller)

    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        username = self.get_argument("username")
        password = self.get_argument("password")
        verify_code_tmp = self.get_argument("verify_code")
        verify_code_client = verify_code_tmp.upper()   # 将验证码字符统一转换成大写
        verify_code_server = VerifyCode.get_verify_code()

        date_kits = DateToolKits()
        logging.info("username:%s password:%s verify_code_client:%s, verify_code_server %s"
                     % (username, password, verify_code_client, verify_code_server))
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()

        if verify_code_server != verify_code_client:
            logging.info("verify code not equal. ")
            response["status"] = False
            response["message"] = "验证码错误！"
            response["data"] = date_kits.get_now_day_str()
            self.write(json.dumps(response))
            return

        auth_flags = UserAuthUtils.authenticate_user_by_name(username, password)

        if(auth_flags == True):
            logging.info("login ok,user name:"+username)
            response["data"] = date_kits.get_now_day_str()

            self.set_current_user(username)
            self.session["authorized"] = True
            render_controller["authorized"] = self.session["authorized"] = True
            self.write(json.dumps(response))
        else:
            logging.info("login failed,user name:" + username)
            render_controller["index"] = False
            render_controller["authorized"] = False
            render_controller["login"] = True
            logging.inf("密码错误处理")
            response["status"] = False
            response["message"] = "密码错误！"
            response["data"] = date_kits.get_now_day_str()

            self.write(json.dumps(response))


class VerifyHandler(BaseHandler):
    def get(self):
        # 生成图片并且返回
        mstream = io.BytesIO()                          # 创建一个BytesIO临时保存生成图片数据
        verify = VerifyImage()
        img = verify.get_image()
        code = verify.get_code()
        VerifyCode.set_verify_code(code)
        img.save(mstream, "PNG")                         # 将返回的验证码图片数据，添加到BytesIO临时保存
        self.write(mstream.getvalue())                  # 从BytesIO临时保存，获取图片返回给img的 src= 进行显示

