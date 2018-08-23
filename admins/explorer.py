#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from handlers.base import BaseHandler
from methods.utils import UserDataUtils
from methods.utils import UserAuthUtils
import json

# 继承 base.py 中的类 BaseHandler


class AdminExplorerHandler(BaseHandler):
    """
    该类处理的主要是登陆后显示的主页和基于主页的操作
    该类只有在登陆成功后才会显示主页页面，登陆失败，不显示该页面
    """

    def get(self):
        # 用户渲染表格模板的数据接口
        # 后续该接口需要从数据库读取
        controller = UserDataUtils.get_render_controller()
        controller["index"] = False
        controller["authorized"] = True
        controller["login"] = False
        controller["admin"] = True
        # username = self.get_argument("user")
        username = self.get_current_user()
        score_tables = UserDataUtils.get_user_score_tables()
        if username != None:
            print("username:" + username)

        role = UserAuthUtils.get_role_by_name(username)
        if role == None:
            role = "admin"
        if controller["admin"] == True:
            self.render("admin_explorer.html", username=username, controller=controller, role=role)

    def post(self):
        pass


class FileDownLoadHandler(BaseHandler):
    def get(self):
        filename = "file/export.xlsx"
        print(filename)
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', ('attachment; filename=%s' % filename).encode('utf-8'))

        with open(filename, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break

                self.write(data)
        # # 记得有finish哦

        self.finish()


class FileUpLoadHandler(BaseHandler):
    def post(self):
        ret = {"status": True, "data": "", "error": "succeed"}
        file_metas = self.request.files["file"]               # 获取上传文件信息
        for meta in file_metas:                                 # 循环文件信息
            file_name = meta['filename']                        # 获取文件的名称
            import os                                           # 引入os路径处理模块
            with open(os.path.join('file', file_name), 'wb') as up:            # os拼接文件保存路径，以字节码模式打开
                up.write(meta['body'])

        self.write(json.dumps(ret))