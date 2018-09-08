#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
from handlers.base import BaseHandler
from methods.utils import UserDataUtils
from methods.controller import PageController


# 继承 base.py 中的类 BaseHandler
class IndexHandler(BaseHandler):
    """
    用户首页处理，显示一些客户不需要登陆也可查看的信息
    """
    def get(self):
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()

        render_controller["index"] = True
        render_controller["authorized"] = self.session["authorized"]
        render_controller["login"] = False
        render_controller["admin"] = self.session["admin"]
        render_controller["organizer"] = self.session["organizer"]

        username = self.get_current_user()
        persons = UserDataUtils.get_user_info_tables()
        self.render("index.html",
                    persons=persons,
                    controller=render_controller,
                    username=username,
                    )

    def post(self):
        pass

