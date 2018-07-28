#!/usr/bin/env Python
# coding=utf-8
"""
the url structure of website
"""
import tornado.web
import sys     #utf-8，兼容汉字

class TableModule(tornado.web.UIModule):
    def render(self, tables):
        return self.render_string("modules/table.html", tables=tables)

class PersonModule(tornado.web.UIModule):
    def render(self, person):
        return self.render_string("modules/person.html", person=person)

    def css_files(self):
        return "css/person.css"

ui = [{"Table": TableModule},
     {"Person": PersonModule}
]