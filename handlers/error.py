#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from methods.controller import PageController
#继承 base.py 中的类 BaseHandler


class ErrorHandler(BaseHandler):
    """
    显示登陆错误的页面
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
        self.render("handlers/error.html", controller=render_controller,
                    language_mapping=self.language_mapping,
                    )
