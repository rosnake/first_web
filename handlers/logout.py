#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
from handlers.base import BaseHandler
import json
import methods.debug as dbg
import sys
from methods.utils import UserDataUtils


class LogoutHandler(BaseHandler):  # 继承 base.py 中的类 BaseHandler
    def get(self):
        # print ("one user name:%s" % one_user)
        print(self.session["authorized"])
        self.clear_current_user()
        self.session["authorized"] = False
        del self.session["username"]
        del self.session["admin"]
        del self.session["organizer"]
        self.redirect('/')
        return

    def post(self):
        pass
