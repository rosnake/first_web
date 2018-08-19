#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from handlers.base import BaseHandler
from methods.utils import UserDataUtils
from methods.utils import UserAuthUtils


#继承 base.py 中的类 BaseHandler

class AdminHandler(BaseHandler):
    """
    该类处理的主要是登陆后显示的主页和基于主页的操作
    该类只有在登陆成功后才会显示主页页面，登陆失败，不显示该页面
    """
    def get(self):
        # 用户渲染表格模板的数据接口
        # 后续该接口需要从数据库读取
        controller = UserDataUtils.get_render_controller()
        controller["index"] = False
        controller["authorized"] = True
        controller["login"] = False
        controller["admin"] = True
        # username = self.get_argument("user")
        username = self.get_current_user()
        score_tables = UserDataUtils.get_user_score_tables()
        if username != None:
            print("username:"+username)

        role = UserAuthUtils.get_role_by_name(username)
        if role == None:
            role="admin"
        if controller["admin"] == True:
            self.render("admin.html", username=username, controller=controller, role=role)

    def post(self):
       pass

