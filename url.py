#!/usr/bin/env Python
# coding=utf-8
"""
the url structure of website
"""

import sys     #utf-8，兼容汉字
reload(sys)
sys.setdefaultencoding("utf-8")
#从相关文件中导入相关处理的类
from handlers.index import IndexHandler
from handlers.user import UserHandler
from handlers.register import RegisterHandler
from handlers.login import LoginHandler
from handlers.home import HomeHandler
from handlers.layer import LayerHandler
from handlers.error import ErrorHandler
from handlers.logout import LogoutHandler
from handlers.statistics import StatHandler
#一个URL列表
url = [
    (r'/', IndexHandler),
    (r'/index', IndexHandler),
    (r'/user', UserHandler),
    (r'/error', ErrorHandler),
    (r'/register', RegisterHandler),
    (r'/login', LoginHandler),
    (r'/logout', LogoutHandler),
    (r'/home', HomeHandler),
    (r'/layer', LayerHandler),
    (r'/statistics', StatHandler),
]