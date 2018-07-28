#!/usr/bin/env Python
# coding=utf-8
"""
the url structure of website
"""

import sys     #utf-8，兼容汉字
reload(sys)
sys.setdefaultencoding("utf-8")

from handlers.index import IndexHandler    #假设已经有了
from handlers.user import UserHandler
from handlers.index import ErrorHandler
from handlers.register import RegisterHandler
from handlers.login import LoginHandler
from handlers.home import HomeHandler

url = [
    (r'/', IndexHandler),
    (r'/user', UserHandler),
    (r'/error', ErrorHandler),
    (r'/register', RegisterHandler),
    (r'/login', LoginHandler),
    (r'/home', HomeHandler),
]