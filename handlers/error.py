#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from base import BaseHandler
#继承 base.py 中的类 BaseHandler
class ErrorHandler(BaseHandler):
    """
    显示登陆错误的页面
    """
    def get(self):
        self.render("error.html")