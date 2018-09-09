#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
from handlers.base import BaseHandler
from methods.controller import PageController


# 继承 base.py 中的类 BaseHandler
class AboutHandler(BaseHandler):
    """
    关于页面处理，显示一些客户不需要登陆也可查看的信息
    """
    def get(self):
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()
        if self.session["authorized"] is None or self.session["authorized"] is False:
            self.redirect("/login?next=/about")
            return

        username = self.get_current_user()

        print(self.session["authorized"])
        render_controller["index"] = False
        render_controller["authorized"] = self.session["authorized"]
        render_controller["login"] = False
        render_controller["admin"] = self.session["admin"]
        render_controller["organizer"] = self.session["organizer"]

        if username is not None:
            self.render("about.html",
                        controller=render_controller,
                        username=username,
                        )
