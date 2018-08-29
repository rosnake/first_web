#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from handlers.base import BaseHandler
from methods.utils import UserDataUtils
from methods.utils import UserAuthUtils
from methods.debug import *
from orm.user import UserModule

#继承 base.py 中的类 BaseHandler

class HomeHandler(BaseHandler):
    """
    该类处理的主要是登陆后显示的主页和基于主页的操作
    该类只有在登陆成功后才会显示主页页面，登陆失败，不显示该页面
    """

    @tornado.web.authenticated
    def get(self):
        # 用户渲染表格模板的数据接口
        # 后续该接口需要从数据库读取
        logging.info(self.session["username"])
        controller = UserDataUtils.get_render_controller()
        controller["index"] = False
        controller["authorized"] = False
        controller["login"] = False

        username = self.get_current_user()
        # 先判断是否完善其他信息，如果没有完善，跳转到信息完善页面
        if username is not None:
            user = self.db.query(UserModule).filter(UserModule.username == username).first()
            if user is not None:
                print(user.username)
                if user.email == "unknown":
                    self.redirect("/user")
                    self.finish()
                    return


        score_tables = UserDataUtils.get_user_score_tables()

        topics_table = UserDataUtils.get_user_topics_table()

        if username is not None:
            controller["authorized"] = True
            print("################"+username)

        role = UserAuthUtils.get_role_by_name(username)
        if role == None:
            role="normal"
        if role == "admin":
            controller["admin"] = True
        else:
            controller["admin"] = False

        print("username:%s,role:%s" % (username, role))
        self.render("home.html", tables=score_tables, controller=controller, topics_table=topics_table, username=username)

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        user_infos = mrd.select_table(table="users",column="*",condition="username", value=username)
        if user_infos:
            db_pwd = user_infos[0][2]
            if db_pwd == password:
                print("username:%s pwd:%s db_pwd %s" % (username, password, db_pwd))
                # 将当前用户名写入 cookie，方法见下面
                self.set_current_user(username)
                self.write(username)
            else:
                print("username:%s pwd:%s " % (username, password))
                self.write("-1")
        else:
            self.write("-1")
