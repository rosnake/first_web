#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
from handlers.base import BaseHandler
from methods.utils import UserDataUtils
from methods.utils import UserAuthUtils
from methods.controller import PageController


# 继承 base.py 中的类 BaseHandler

class IssuesHandler(BaseHandler):
    """
    该类处理的主要是登陆后显示的主页和基于主页的操作
    该类只有在登陆成功后才会显示主页页面，登陆失败，不显示该页面
    """
    def get(self):
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()
        if self.session["authorized"] is None or self.session["authorized"] is False:
            self.redirect("/login?next=/issues")
            return

        username = self.get_current_user()

        print(self.session["authorized"])
        render_controller["index"] = False
        render_controller["authorized"] = self.session["authorized"]
        render_controller["login"] = False
        render_controller["admin"] = self.session["admin"]
        render_controller["organizer"] = self.session["organizer"]

        if username is not None:
            self.render("issues.html")

    def post(self):
        pass

