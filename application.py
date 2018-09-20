#!/usr/bin/env Python
# coding=utf-8

from url import url
from ui_mapping import ui
import tornado.web
import os
from config.debug import DebugConfig

settings = dict(
    web_title=u"Learning System",
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "statics"),
    cookie_secret="vEg+O43NQwGknl6vRwKRwPajAP/RKUSKsGKLhY5j0MI=",
    xsrf_cookies=True,
    login_url='/login',
    
    )

application = tornado.web.Application(
    handlers=url,
    ui_modules=ui,
    debug=DebugConfig.DEBUG,
    **settings
    )
