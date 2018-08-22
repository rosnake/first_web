#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from base import BaseHandler
from  methods.utils import UserDataUtils
from  methods.utils import UserAuthUtils


# 继承 base.py 中的类 BaseHandler

class StatHandler(BaseHandler):
    """
    该类处理的主要是登陆后显示的主页和基于主页的操作
    该类只有在登陆成功后才会显示主页页面，登陆失败，不显示该页面
    """
    def get(self):
        # 用户渲染表格模板的数据接口
        # 后续该接口需要从数据库读取
        username=self.get_current_user()
        controller = UserDataUtils.get_render_controller()
        controller["index"] = False
        controller["authorized"] = False
        controller["login"] = False

        user_score = UserDataUtils.get_user_score_by_name(username)
        exchange_presents_table = UserDataUtils.get_exchange_presents_table()
        if username != None:
            controller["authorized"] = True
            print("################"+username)

        self.render("statistics.html", user_score=user_score, controller=controller, username=username,
                    presents_table=exchange_presents_table)

    def post(self):
        pass
