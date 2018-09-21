#! /usr/bin/env python
# coding=utf-8

import tornado.web
from session.session import SessionFactory
from methods.debug import *
from orm.db_base import dbSession
from orm.users_info import UsersInfoModule
from config.language import LanguageMapping
from methods.controller import PageController


class BaseHandler(tornado.web.RequestHandler):
    """
    该类为用户提供web请求处理的基本处理操作，主要包括以下操作：
    1、数据库操作
    2、安全认证操作
    """
    """
    该方法提供session初始化
    """
    def initialize(self):
        logging.info("[initialize]:get session handler and init db")
        self.session = SessionFactory.get_session_handler(self)
        self.db = dbSession
        # 准备多语言
        self.language_mapping = LanguageMapping().get_mapping_table()
        # 准备页面控制器
        page_controller = PageController()
        self.render_controller = page_controller.get_render_controller()

    def on_finish(self):
        logging.info("[finish]:clear cookie and close db")
        self.db.close()
        self.clear_cookie("user_name")

    def get_current_user(self):
        user_id = self.get_secure_cookie("user_name")
        if not user_id:
            logging.info("[cookie]:get current user is None")
            return None
        # 设置的时候用了json编码，获取的时候对应的需要解码
        user = tornado.escape.json_decode(user_id)
        logging.info("[cookie]:current login user is :"+user)

        return user

    def set_current_user(self, user):
        if user:
            # 注意这里使用了 tornado.escape.json_encode() 方法
            self.set_secure_cookie('user_name', tornado.escape.json_encode(user))
            logging.info("set user [%s] to cookies." % ( user ))
        else:
            self.clear_cookie("user_name")

    def clear_current_user(self):
        logging.info("[cookie]:clear cookies")
        self.clear_cookie("user_name")

    def get_user_role(self, user_name):
        user = self.db.query(UsersInfoModule).filter(UsersInfoModule.user_name == user_name).first()

        if user is None:
            return False, False

        if user.user_role == "admin":
            return True, False
        elif user.user_role == "organizer":
            return False, True
        else:
            return False, False

