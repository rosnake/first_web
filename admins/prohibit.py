#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from methods.controller import PageController


#继承 base.py 中的类 BaseHandler

class AdminProhibitHandler(BaseHandler):
    """
    该类处理的主要是登陆后显示的主页和基于主页的操作
    该类只有在登陆成功后才会显示主页页面，登陆失败，不显示该页面
    """
    def get(self):
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()

        print(self.session["authorized"])
        render_controller["index"] = False
        render_controller["authorized"] = self.session["authorized"]
        render_controller["login"] = False
        render_controller["admin"] = self.session["admin"]
        render_controller["organizer"] = self.session["organizer"]
        self.render("admin/prohibit.html", controller=render_controller)

    def post(self):
        pass

