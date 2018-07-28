#!/usr/bin/env Python
# coding=utf-8

from url import url
from ui import ui
import tornado.web
import os

settings = dict(
    web_title=u"Python Learning",
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "statics"),
    cookie_secret = "vEg+O43NQwGknl6vRwKRwPajAP/RKUSKsGKLhY5j0MI=",
    xsrf_cookies = True,
    login_url = '/',
    
    )

application = tornado.web.Application(
    handlers = url,
    ui_modules=ui,
	debug = True,
    **settings
    )