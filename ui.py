#!/usr/bin/env Python
# coding=utf-8
"""
the UI modules  of website
"""
import tornado.web
import sys     #utf-8，兼容汉字

#表格模板
class TableModule(tornado.web.UIModule):
    def render(self, tables, role):
        return self.render_string("modules/table.html", tables=tables, role=role)

#人员信息模板
class PersonModule(tornado.web.UIModule):
    def render(self, person):
        return self.render_string("modules/person.html", person=person)

    def css_files(self):
        return "css/person.css"
#导航模板
class NavigationModule(tornado.web.UIModule):
    def render(self):
        return self.render_string("modules/navigation.html")

    def css_files(self):
        return "css/navigation.css"
#UI模板入口
ui = [{"Table": TableModule},
     {"Person": PersonModule},
     {"Navigation": NavigationModule}
]