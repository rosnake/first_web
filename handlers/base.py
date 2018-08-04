#! /usr/bin/env python
# coding=utf-8

import tornado.web
import methods.readdb as orm
class BaseHandler(tornado.web.RequestHandler):
    """
    该类为用户提供web请求处理的基本处理操作，主要包括以下操作：
    1、数据库操作
    2、安全认证操作
    """

    def get_current_user(self):
        user_id = self.get_secure_cookie("username")
        if not user_id:
            print("None=======")
            return None

        return user_id
    
  
        
    def set_current_user(self, user):
        if user:
            self.set_secure_cookie('username', tornado.escape.json_encode(user))    #注意这里使用了 tornado.escape.json_encode() 方法
        else:
            self.clear_cookie("username")

    def clear_current_user(self):
        self.clear_cookie("username")