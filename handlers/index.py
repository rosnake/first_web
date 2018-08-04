#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from base import BaseHandler
from  methods.utils import UserDataUtils
#继承 base.py 中的类 BaseHandler
class IndexHandler(BaseHandler):
    """
    用户首页处理，显示一些客户不需要登陆也可查看的信息
    """
    def get(self):
        usernames = mrd.select_columns(table="users",column="username")
        one_user = usernames[0][0]
        #print ("one user name:%s" % one_user)
        username=self.get_current_user()
        controller = UserDataUtils.get_render_controller()
        controller["index"] = True
        controller["authorized"] = False
        controller["login"] = False

        if username != None:
            controller["authorized"] = True
            print("################"+username)

        self.render("index.html",
                    persons=[
                        {
                            "name": "chenhaha",
                            "image": "images/chenhaha.jpg",
                            "remnants":11,
                            "sub": -8,
                            "add": 12,
                            "description": "<p>这世界要是没有爱情，它在我们心中还会有什么意义！这就如一盏没有亮光的走马灯</p>"
                        },
                        {
                            "name": "raohaha",
                            "image": "images/raohaha.jpg",
                            "remnants": 10,
                            "sub": -9,
                            "add": 15,
                            "description":"<p>菩提本无树，明镜亦非台</p>"
                        }
                    ],
                    controller =controller,
                    username=username,
                    )

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        user_infos = mrd.select_table(table="users",column="*",condition="username",value=username)
        if user_infos:
            db_pwd = user_infos[0][2]
            if db_pwd == password:
                print("username:%s pwd:%s db_pwd %s" % (username, password, db_pwd))
                self.set_current_user(username)    #将当前用户名写入 cookie，方法见下面
                self.write(username)
            else:
                print("username:%s pwd:%s " % (username, password))
                self.write("-1")
        else:
            self.write("-1")
