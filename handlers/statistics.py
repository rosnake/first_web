#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from base import BaseHandler
from  methods.utils import UserDataUtils
from  methods.utils import UserAuthUtils


#继承 base.py 中的类 BaseHandler

class StatHandler(BaseHandler):
    """
    该类处理的主要是登陆后显示的主页和基于主页的操作
    该类只有在登陆成功后才会显示主页页面，登陆失败，不显示该页面
    """
    def get(self):
        #用户渲染表格模板的数据接口
        #后续该接口需要从数据库读取
        controller = UserDataUtils.get_render_controller()
        controller["index"] = False
        controller["authorized"] = True
        controller["login"] = False
        score_tables= [
                {"name": "raoyuanqin","late": -1,"retreat": 0,"absenteeism": 0,"un_present": 0,"total": 10 },
                {"name": "chenmeijing","late": -1,"retreat": 0,"absenteeism": 0,"un_present": 0,"total": 11 },
                {"name": "chenxiaojie","late": -1,"retreat": 0,"absenteeism": -1,"un_present": 0,"total": 9 },
                {"name": "raoxiansheng","late": -1,"retreat": -1,"absenteeism": 0,"un_present": 0,"total": 12 },
            ]

        role="normal"

        self.render("home.html", tables=score_tables, controller=controller, role=role)

    def post(self):
        pass
