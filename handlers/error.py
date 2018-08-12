#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from handlers.base import BaseHandler
from  methods.utils import UserDataUtils
#继承 base.py 中的类 BaseHandler
class ErrorHandler(BaseHandler):
    """
    显示登陆错误的页面
    """
    controller = UserDataUtils.get_render_controller()
    controller["index"] = True
    controller["authorized"] = False

    def get(self):
        self.render("error.html", controller=controller)