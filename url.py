#!/usr/bin/env Python
# coding=utf-8
"""
the url structure of website
"""
# utf-8，兼容汉字
import sys
import importlib
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
from handlers.feedback import FeedBackHandler
from admins.admin import AdminHandler
from admins.topics import AdminTopicsHandler
from admins.discipline import AdminDisciplineHandler
from admins.exchange import AdminExchangeHandler
from admins.member import AdminMemberHandler
from admins.organizer import AdminOrganizerHandler
from admins.credits import AdminCreditsHandler
from admins.issues import AdminIssuesHandler
from admins.issues_modify import AdminIssuesModifyHandler
from admins.explorer import AdminExplorerHandler
from admins.explorer import FileDownLoadHandler
from admins.explorer import FileUpLoadHandler
from admins.meeting import AdminMeetingHandler
from admins.attendance import AdminAttendanceHandler
from admins.prohibit import AdminProhibitHandler
from admins.evaluation import AdminEvaluatingHandler
from admins.history import AdminHistoryHandler
from admins.opinions import AdminOpinionsHandler
from admins.opinions_popup import AdminOpinionsPopupHandler
importlib.reload(sys)

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
    (r'/feedback', FeedBackHandler),
    (r'/admin/topics', AdminTopicsHandler),
    (r'/admin/credits', AdminCreditsHandler),
    (r'/admin/organizer', AdminOrganizerHandler),
    (r'/admin/member', AdminMemberHandler),
    (r'/admin/discipline', AdminDisciplineHandler),
    (r'/admin/exchange', AdminExchangeHandler),
    (r'/admin/issues', AdminIssuesHandler),
    (r'/admin/issues_modify', AdminIssuesModifyHandler),
    (r'/admin/explorer', AdminExplorerHandler),
    (r'/admin/meeting', AdminMeetingHandler),
    (r'/file/download', FileDownLoadHandler),
    (r'/file/upload', FileUpLoadHandler),
    (r'/admin/attendance', AdminAttendanceHandler),
    (r'/admin/prohibit', AdminProhibitHandler),
    (r'/admin/evaluating', AdminEvaluatingHandler),
    (r'/admin/history', AdminHistoryHandler),
    (r'/admin/opinions', AdminOpinionsHandler),
    (r'/admin/opinions_popup', AdminOpinionsPopupHandler),
]
