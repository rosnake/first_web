#! /usr/bin/env python
# coding=utf-8
"""
定义页面渲染默认控制现，当前页面可以根据不同的角色控制不同的可见内容
"""


class PageController:

    def __init__(self):
        self.render_controller = {"index": False, "login": False, "authorized": False, "admin": False,
                                  "organizer": False}

    def get_render_controller(self):
        return self.render_controller
