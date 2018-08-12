#! /usr/bin/env python
# coding=utf-8

import tornado.web
import methods.readdb as orm
# from  methods.session import  Session


class BaseHandler(tornado.web.RequestHandler):
    """
    该类为用户提供web请求处理的基本处理操作，主要包括以下操作：
    1、数据库操作
    2、安全认证操作
    """

    def get_current_user(self):
        user_id = self.get_secure_cookie("username")
        if not user_id:
            print("get current user is None")
            return None
        # 设置的时候用了json编码，获取的时候对应的需要解码
        user = tornado.escape.json_decode(user_id)
        print("current login user is :"+user)

        return user

    def set_current_user(self, user):
        if user:
            # 注意这里使用了 tornado.escape.json_encode() 方法
            self.set_secure_cookie('username', tornado.escape.json_encode(user))
            print("set user [%s] to cookies." %(user))
        else:
            self.clear_cookie("username")

    def clear_current_user(self):
        print("clear cookies")
        self.clear_cookie("username")

