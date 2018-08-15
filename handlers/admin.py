#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from base import BaseHandler
from  methods.utils import UserDataUtils
from  methods.utils import UserAuthUtils


#继承 base.py 中的类 BaseHandler

class AdminHandler(BaseHandler):
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
        controller["admin"] = True
        #username = self.get_argument("user")
        username = self.get_current_user()
        score_tables = UserDataUtils.get_user_score_tables()
        if username != None:
            print("username:"+username)

        role = UserAuthUtils.get_role_by_name(username)
        if role == None:
            role="admin"
        if controller["admin"] == True:
            self.render("admin.html", username=username, controller=controller, role=role)

    def post(self):
       pass


# 继承 base.py 中的类 BaseHandler
class AdminMemberHandler(BaseHandler):
    """
    用户首页处理，显示一些客户不需要登陆也可查看的信息
    """
    def get(self):
        usernames = mrd.select_columns(table="users",column="username")
        one_user = usernames[0][0]
        # print ("one user name:%s" % one_user)
        username = self.get_current_user()
        controller = UserDataUtils.get_render_controller()
        controller["index"] = True
        controller["authorized"] = False
        controller["login"] = False

        if username is not None:
            controller["authorized"] = True
            print("################"+username)

        user_tables = UserAuthUtils.get_user_info_tables()
        self.render("admin_member.html",
                    user_tables=user_tables,
                    controller=controller,
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
                self.set_current_user(username)    # 将当前用户名写入 cookie，方法见下面
                self.write(username)
            else:
                print("username:%s pwd:%s " % (username, password))
                self.write("-1")
        else:
            self.write("-1")


# 继承 base.py 中的类 BaseHandler
class AdminOrganizerHandler(BaseHandler):
    """
    用户首页处理，显示一些客户不需要登陆也可查看的信息
    """
    def get(self):
        usernames = mrd.select_columns(table="users",column="username")
        one_user = usernames[0][0]
        # print ("one user name:%s" % one_user)
        username = self.get_current_user()
        controller = UserDataUtils.get_render_controller()
        controller["index"] = True
        controller["authorized"] = False
        controller["login"] = False

        if username is not None:
            controller["authorized"] = True
            print("################"+username)

        persons = UserDataUtils.get_user_info_tables()
        self.render("admin_organizer.html",
                    persons = persons,
                    controller = controller,
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
                self.set_current_user(username)    # 将当前用户名写入 cookie，方法见下面
                self.write(username)
            else:
                print("username:%s pwd:%s " % (username, password))
                self.write("-1")
        else:
            self.write("-1")


# 继承 base.py 中的类 BaseHandler
class AdminPointHandler(BaseHandler):
    """
    用户首页处理，显示一些客户不需要登陆也可查看的信息
    """
    def get(self):
        usernames = mrd.select_columns(table="users",column="username")
        one_user = usernames[0][0]
        # print ("one user name:%s" % one_user)
        username = self.get_current_user()
        controller = UserDataUtils.get_render_controller()
        controller["index"] = True
        controller["authorized"] = False
        controller["login"] = False

        if username is not None:
            controller["authorized"] = True
            print("################"+username)

        persons = UserDataUtils.get_user_info_tables()
        self.render("admin_point.html",
                    persons = persons,
                    controller = controller,
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
                self.set_current_user(username)    # 将当前用户名写入 cookie，方法见下面
                self.write(username)
            else:
                print("username:%s pwd:%s " % (username, password))
                self.write("-1")
        else:
            self.write("-1")


# 继承 base.py 中的类 BaseHandler
class AdminTopicsHandler(BaseHandler):
    """
    用户首页处理，显示一些客户不需要登陆也可查看的信息
    """
    def get(self):
        usernames = mrd.select_columns(table="users",column="username")
        one_user = usernames[0][0]
        # print ("one user name:%s" % one_user)
        username = self.get_current_user()
        controller = UserDataUtils.get_render_controller()
        controller["index"] = True
        controller["authorized"] = False
        controller["login"] = False

        if username is not None:
            controller["authorized"] = True
            print("################"+username)

        persons = UserDataUtils.get_user_info_tables()
        self.render("admin_topics.html",
                    persons = persons,
                    controller = controller,
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
                self.set_current_user(username)    # 将当前用户名写入 cookie，方法见下面
                self.write(username)
            else:
                print("username:%s pwd:%s " % (username, password))
                self.write("-1")
        else:
            self.write("-1")

