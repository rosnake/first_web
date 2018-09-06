#!/usr/bin/env Python
# coding=utf-8
"""
the url structure of website
"""
# utf-8，兼容汉字
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# 从相关文件中导入相关处理的类
from handlers.index import IndexHandler
from handlers.about import AboutHandler
from handlers.user import UserHandler
from handlers.register import RegisterHandler
from handlers.login import LoginHandler
from handlers.home import HomeHandler
from handlers.layer import LayerHandler
from handlers.error import ErrorHandler
from handlers.logout import LogoutHandler
from handlers.statistics import StatHandler
from handlers.topics import TopicsHandler
from handlers.applications import ApplicationsHandler
from handlers.issues import IssuesHandler
from handlers.login import VerifyHandler
from handlers.modify_pwd import ModifyPassWordHandler
from admins.admin import AdminHandler
from admins.topics import AdminTopicsHandler
from admins.deduct import AdminDeductHandler
from admins.exchange import AdminExchangeHandler
from admins.member import AdminMemberHandler
from admins.organizer import AdminOrganizerHandler
from admins.points import AdminPointHandler
from admins.issues import AdminIssuesHandler
from admins.issues_modify import AdminIssuesModifyHandler
from admins.explorer import AdminExplorerHandler
from admins.explorer import FileDownLoadHandler
from admins.explorer import FileUpLoadHandler
from admins.meeting import AdminMeetingHandler
from admins.attendance import AdminAttendanceHandler

# 一个URL列表
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
    (r'/topics', TopicsHandler),
    (r'/applications', ApplicationsHandler),
    (r'/issues', IssuesHandler),
    (r'/verify_code', VerifyHandler),
    (r'/modify_password', ModifyPassWordHandler),
    (r'/admin', AdminHandler),
    (r'/about', AboutHandler),
    (r'/admin/topics', AdminTopicsHandler),
    (r'/admin/point', AdminPointHandler),
    (r'/admin/organizer', AdminOrganizerHandler),
    (r'/admin/member', AdminMemberHandler),
    (r'/admin/deduct', AdminDeductHandler),
    (r'/admin/exchange', AdminExchangeHandler),
    (r'/admin/issues', AdminIssuesHandler),
    (r'/admin/issues_modify', AdminIssuesModifyHandler),
    (r'/admin/explorer', AdminExplorerHandler),
    (r'/admin/meeting', AdminMeetingHandler),
    (r'/file/download', FileDownLoadHandler),
    (r'/file/upload', FileUpLoadHandler),
    (r'/admin/attendance', AdminAttendanceHandler),
]
