#!/usr/bin/env Python
# coding=utf-8

from methods.debug import *
from handlers.base import BaseHandler
import json
import io  # 导入io模块
from methods.image_generator import VerifyImage  # 导入验证码图片生成插件
from methods.controller import PageController  # 导入页面控制器
from methods.toolkits import DateToolKits
from orm.users_info import UsersInfoModule
from config.debug import DebugConfig


# 继承 base.py 中的类 BaseHandler
class LoginHandler(BaseHandler):

    def get(self):
        next_name = self.get_argument('next', '')
        logging.info("login next name:" + next_name)
        self.clear_current_user()
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()
        render_controller["index"] = False
        render_controller["login"] = True
        render_controller["authorized"] = False

        logging.info("get login page")
        self.render("login.html", controller=render_controller, nextname=next_name,
                    language_mapping=self.language_mapping,
                    )

    def post(self):
        response = {"status": True, "data": "", "message": "failed"}

        user_name = self.get_argument("user_name")
        pass_word = self.get_argument("password")
        nextname = self.get_argument("next")
        logging.info("next name:" + nextname)
        verify_code_tmp = self.get_argument("verify_code")
        verify_code_client = verify_code_tmp.upper()  # 将验证码字符统一转换成大写
        verify_code_server = self.session["verify_code"]

        date_kits = DateToolKits()
        logging.info("user_name:%s password:%s verify_code_client:%s, verify_code_server %s"
                     % (user_name, pass_word, verify_code_client, verify_code_server))
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()

        # 为了调试，注销验证码验证
        if DebugConfig.DEBUG is True:
            verify_code_client = verify_code_server

        if verify_code_server != verify_code_client:
            logging.info("verify code not equal. ")
            response["status"] = False
            response["message"] = "验证码错误！"
            response["data"] = date_kits.get_now_day_str()
            self.write(json.dumps(response))
            return

        del self.session["verify_code"]

        _user_name = self.db.query(UsersInfoModule).filter(UsersInfoModule.user_name == user_name).first()

        if _user_name is None:
            logging.info("login failed,user name:" + user_name + "is not exist")
            render_controller["index"] = False
            render_controller["authorized"] = False
            render_controller["login"] = True
            logging.info("用户名不存在")
            response["status"] = False
            response["message"] = "用户名不存在！"
            response["data"] = date_kits.get_now_day_str()

            self.write(json.dumps(response))
            return

        user = self.db.query(UsersInfoModule).filter(UsersInfoModule.user_name == user_name).filter(
            UsersInfoModule.pass_word == pass_word).first()
        print(user)
        if user is not None:
            logging.info("login ok,user name:" + user_name)
            response["data"] = date_kits.get_now_day_str()
            admin, organizer = self.get_user_role(user_name)
            self.set_current_user(user_name)
            self.session["authorized"] = True
            self.session["user_name"] = user_name
            self.session["admin"] = admin
            self.session["organizer"] = organizer
            render_controller["authorized"] = self.session["authorized"] = True
            self.write(json.dumps(response))
            return
        else:
            logging.info("login failed,user name:" + user_name)
            render_controller["index"] = False
            render_controller["authorized"] = False
            render_controller["login"] = True
            logging.info("密码错误处理")
            response["status"] = False
            response["message"] = "密码错误！"
            response["data"] = date_kits.get_now_day_str()

            self.write(json.dumps(response))
            return


class VerifyHandler(BaseHandler):
    def get(self):
        # 生成图片并且返回
        mstream = io.BytesIO()  # 创建一个BytesIO临时保存生成图片数据
        verify = VerifyImage()
        img = verify.get_image()
        code = verify.get_code()
        self.session["verify_code"] = code
        img.save(mstream, "PNG")  # 将返回的验证码图片数据，添加到BytesIO临时保存
        self.write(mstream.getvalue())  # 从BytesIO临时保存，获取图片返回给img的 src= 进行显示
