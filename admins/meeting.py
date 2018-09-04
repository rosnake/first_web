#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from handlers.base import BaseHandler
from methods.utils import UserDataUtils
from methods.utils import UserAuthUtils
from methods.controller import PageController
from methods.toolkits import DateToolKits


# 继承 base.py 中的类 BaseHandler
class AdminMeetingHandler(BaseHandler):
    """
    用户首页处理，显示一些客户不需要登陆也可查看的信息
    """
    def get(self):
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()
        if self.session["authorized"] is None or self.session["authorized"] is False:
            self.redirect("/login?next=/admin/meeting")
            return

        render_controller["index"] = False
        render_controller["authorized"] = self.session["authorized"]
        render_controller["login"] = False
        render_controller["admin"] = self.session["admin"]
        render_controller["organizer"] = self.session["organizer"]

        username = self.get_current_user()
        if username is not None:
            meeting_tables = UserDataUtils.get_meeting_tables()
            self.render("admin/meeting.html",
                        meeting_tables=meeting_tables,
                        controller=render_controller,
                        username=username,
                        )

    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()

