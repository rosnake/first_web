#!/usr/bin/env Python
# coding=utf-8
"""
the UI modules  of website
"""
import tornado.web


# 导航模板
class NavigationModule(tornado.web.UIModule):
    def render(self, controller, language_mapping):
        return self.render_string("modules/navigation.html", controller=controller, language_mapping=language_mapping)

    def css_files(self):
        return "css/navigation.css"


# 导航模板
class AdminSidebarModule(tornado.web.UIModule):
    def render(self, controller, language_mapping):
        return self.render_string("modules/admin_sidebar.html", controller=controller, language_mapping=language_mapping)

    def css_files(self):
        return "css/admin.css"


# 头模板
class HeaderModule(tornado.web.UIModule):
    def render(self, user_name, language_mapping):
        return self.render_string("modules/header.html", user_name=user_name, language_mapping=language_mapping)

    def css_files(self):
        return "css/header.css"


# 话题自目录
class SubtitleModule(tornado.web.UIModule):
    def render(self, user_name, language_mapping):
        return self.render_string("modules/topic_subtitle.html", user_name=user_name, language_mapping=language_mapping)

    def css_files(self):
        return "css/subtitle.css"

