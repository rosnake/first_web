#!/usr/bin/env Python
# coding=utf-8

import json
from methods.toolkits import DateToolKits
from methods.debug import *
# 导入页面控制器
from methods.controller import PageController

"""
该装饰器用户用户访问页面的权限管理。
1、如果用户未登录会跳转到登录页面。
2、如果用户登录后没有相关权限，会跳转到权限提示页面。
3、如果用户权限都有，完成页面控制器初始化
"""


def admin_get_auth(jump_page, admin_only):
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            logging.info('[decorator]:decorator is running,jump page is '+jump_page)
            #  1、判断是否有登录，没有登录，跳转到登录界面
            if self.session["authorized"] is None or self.session["authorized"] is False:
                self.redirect("/login?next="+jump_page)
                return

            # 2、只有管理员有权限的页面只需判断管理员权限即可
            if admin_only is True:
                logging.info("[decorator]:admin only is true")
                if self.session["admin"] is None or self.session["admin"] is False:
                    self.redirect("/admin/prohibit")
                    logging.warning("[decorator]:current user is No admin")
                    return

            #  3、其他页面需要判断管理权限或者组织者权限
            if self.session["admin"] is None or self.session["admin"] is False:
                if self.session["organizer"] is None or self.session["organizer"] is False:
                    self.redirect("/admin/prohibit")
                    logging.warning("[decorator]:current user is No admin or organizer")
                    return

            #  4、完成页面控制器的初始化
            logging.info("[decorator]:prepare page controller")
            page_controller = PageController()
            self.render_controller = page_controller.get_render_controller()
            self.render_controller["index"] = False
            self.render_controller["login"] = False
            if self.session["authorized"] is not None:
                self.render_controller["authorized"] = self.session["authorized"]
            else:
                self.render_controller["authorized"] = False

            if self.session["admin"] is not None:
                self.render_controller["admin"] = self.session["admin"]
            else:
                self.render_controller["admin"] = False

            if self.session["organizer"] is not None:
                self.render_controller["organizer"] = self.session["organizer"]
            else:
                self.render_controller["organizer"] = False

            logging.info("[decorator]:authorized=%s, admin=%s, organizer=%s" % (str(self.render_controller["authorized"]),
                                                                    str(self.render_controller["admin"]),
                                                                    str(self.render_controller["organizer"]),
                                                                    ))
            if self.session["user_name"] is not None:
                logging.info("[decorator]:current user is [%s]" % self.session["user_name"])

            return method(self, *args, **kwargs)
        return wrapper
    return decorator


def admin_post_auth(admin_only):
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            logging.info("[decorator]:post authorization")
            response = {"status": True, "data": "", "message": "failed"}
            date_kits = DateToolKits()
            response["data"] = date_kits.get_now_day_str()
            response["status"] = False
            response["message"] = "无权限操作！"

            #  1、判断是否有登录，没有登录
            if self.session["authorized"] is None or self.session["authorized"] is False:
                self.write(json.dumps(response))
                return

            # 2、只有管理员有权限的页面只需判断管理员权限即可
            if admin_only is True:
                logging.info("[decorator]:admin only is true")
                if self.session["admin"] is None or self.session["admin"] is False:
                    self.write(json.dumps(response))
                    logging.warning("[decorator]:current user is No admin")
                    return

            #  3、其他页面需要判断管理权限或者组织者权限
            if self.session["admin"] is None or self.session["admin"] is False:
                if self.session["organizer"] is None or self.session["organizer"] is False:
                    self.write(json.dumps(response))
                    logging.warning("[decorator]:current user is No admin or organizer")
                    return

            return method(self, *args, **kwargs)
        return wrapper
    return decorator
