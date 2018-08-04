#!/usr/bin/env Python
# coding=utf-8

import tornado.web
import tornado.escape
import methods.readdb as mrd
from base import BaseHandler
from  methods.utils import UserDataUtils

class UserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        controller = UserDataUtils.get_render_controller()
        controller["index"] = True
        controller["authorized"] = False
        #username = self.get_argument("user")
        username = tornado.escape.json_decode(self.current_user)
        user_infos = mrd.select_table(table="users",column="*",condition="username",value=username)
        self.render("user.html", users = user_infos, controller=controller)