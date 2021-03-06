#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from handlers.decorator import handles_get_auth


# 继承 base.py 中的类 BaseHandler
class AboutHandler(BaseHandler):
    """
    关于页面处理，显示关于信息
    """
    @handles_get_auth("/about")
    def get(self):
        user_name = self.get_current_user()

        if user_name is not None:
            self.render("handlers/about.html",
                        controller=self.render_controller,
                        user_name=user_name,
                        language_mapping=self.language_mapping,
                        )
