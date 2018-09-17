#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
import json
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth

# 继承 base.py 中的类 BaseHandler


class AdminExplorerHandler(BaseHandler):
    """
    该类用户文件管理，主要用户导入导出功能
    """
    @admin_get_auth("/admin/explorer", True)
    def get(self):
        user_name = self.get_current_user()
        if user_name is not None:
            self.render("admin/explorer.html", user_name=user_name, controller=self.render_controller)

    @admin_post_auth(False)
    def post(self):
        pass


class FileDownLoadHandler(BaseHandler):
    @admin_get_auth("/admin/explorer", True)
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