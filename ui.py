#!/usr/bin/env Python
# coding=utf-8
"""
the UI modules  of website
"""
import tornado.web
import sys     # utf-8，兼容汉字


# 人员信息模板
class PersonModule(tornado.web.UIModule):
    def render(self, person):
        return self.render_string("modules/person.html", person=person)

    def css_files(self):
        return "css/person.css"


# 导航模板
class NavigationModule(tornado.web.UIModule):
    def render(self, controller):
        return self.render_string("modules/navigation.html", controller=controller)

    def css_files(self):
        return "css/navigation.css"


# 导航模板
class AdminModule(tornado.web.UIModule):
    def render(self, controller):
        return self.render_string("modules/admin_navigation.html", controller=controller)

    def css_files(self):
        return "css/admin.css"


# 头模板
class HeaderModule(tornado.web.UIModule):
    def render(self, user_name):
        return self.render_string("modules/header.html", user_name=user_name)

    def css_files(self):
        return "css/header.css"


# UI模板入口
ui = [
    {"Person": PersonModule},
    {"Navigation": NavigationModule, },
    {"Admin": AdminModule, },
    {"Header": HeaderModule, }
    ]

