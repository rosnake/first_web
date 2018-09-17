#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from handlers.decorator import handles_get_auth
from handlers.decorator import handles_post_auth

# 继承 base.py 中的类 BaseHandler

class IssuesHandler(BaseHandler):
    """
    该类处理的主要是登陆后显示的主页和基于主页的操作
    该类只有在登陆成功后才会显示主页页面，登陆失败，不显示该页面
    """
    @handles_get_auth("/issues")
    def get(self):
        user_name = self.get_current_user()
        if user_name is not None:
            self.render("issues.html")

    @handles_post_auth
    def post(self):
        pass

