#!/usr/bin/env Python
# coding=utf-8

#  多语言处理


class LanguageMapping:
    language_mapping_chinese = {
        "member":           {"link": "/admin/member",       "name": "成员管理"},
        "discipline":       {"link": "/admin/discipline",   "name": "积分项管理"},
        "exchange":         {"link": "/admin/exchange",     "name": "积分兑换"},
        "explorer":         {"link": "/admin/explorer",     "name": "文件管理"},
        "topics":           {"link": "/admin/topics",       "name": "话题管理"},
        "credits":          {"link": "/admin/credits",      "name": "积分管理"},
        "organizer":        {"link": "/admin/organizer",    "name": "组织者管理"},
        "meeting":          {"link": "/admin/meeting",      "name": "会议管理"},
        "attendance":       {"link": "/admin/attendance",   "name": "出勤管理"},
        "evaluating":       {"link": "/admin/evaluating",   "name": "评价管理"},
        "history":          {"link": "/admin/history",      "name": "操作历史"},
        "opinions":         {"link": "/admin/opinions",     "name": "意见管理"},

        "index":            {"link": "/index",              "name": "首页"},
        "home":             {"link": "/home",               "name": "个人主页"},
        "issues":           {"link": "/topics",             "name": "议题信息"},
        "statistics":       {"link": "/statistics",         "name": "我的积分"},
        "apply":            {"link": "/applications",       "name": "议题申报"},
        "admin":            {"link": "/admin",              "name": "管理"},
        "about":            {"link": "/about",              "name": "关于"},
        "feedback":         {"link": "/feedback",           "name": "意见反馈"},

        "login":            {"link": "/about",              "name": "登录"},
        "register":         {"link": "/register",           "name": "注册"},
        "mod_pwd":          {"link": "/modify_password",    "name": "修改密码"},
        "logout":           {"link": "/logout",             "name": "退出"},

        "current_topic":    {"link": "/topics",              "name": "本周议题"},
        "history_topic":    {"link": "/topics/history",      "name": "历史议题"},
        "evaluation_topic": {"link": "/topics/evaluation",   "name": "待评价议题"},
        "assessment_topic": {"link": "/topics/assessment",   "name": "已申请议题"},
    }

    language_mapping_english = {
        "member":           {"link": "/admin/member",       "name": "member"},
        "discipline":       {"link": "/admin/discipline",   "name": "discipline"},
        "exchange":         {"link": "/admin/exchange",     "name": "exchange"},
        "explorer":         {"link": "/admin/explorer",     "name": "explorer"},
        "topics":           {"link": "/admin/topics",       "name": "topics"},
        "credits":          {"link": "/admin/credits",      "name": "credits"},
        "organizer":        {"link": "/admin/organizer",    "name": "organizer"},
        "meeting":          {"link": "/admin/meeting",      "name": "meeting"},
        "attendance":       {"link": "/admin/attendance",   "name": "attendance"},
        "evaluating":       {"link": "/admin/evaluating",   "name": "evaluating"},
        "history":          {"link": "/admin/history",      "name": "history"},
        "opinions":         {"link": "/admin/opinions",     "name": "opinions"},

        "index":            {"link": "/index",              "name": "index"},
        "home":             {"link": "/home",               "name": "home"},
        "issues":           {"link": "/topics",             "name": "topics"},
        "statistics":       {"link": "/statistics",         "name": "statistics"},
        "apply":            {"link": "/applications",       "name": "applications"},
        "admin":            {"link": "/admin",              "name": "admin"},
        "about":            {"link": "/about",              "name": "about"},
        "feedback":         {"link": "/feedback",           "name": "feedback"},

        "login":            {"link": "/login",              "name": "login"},
        "register":         {"link": "/register",           "name": "register"},
        "mod_pwd":          {"link": "/modify_password",    "name": "mod_pwd"},
        "logout":           {"link": "/logout",             "name": "logout"},

        "current_topic":    {"link": "/topics",              "name": "current topic"},
        "history_topic":    {"link": "/topics/history",      "name": "history topic"},
        "evaluation_topic": {"link": "/topics/evaluation",   "name": "evaluation topic"},
        "assessment_topic": {"link": "/topics/assessment",   "name": "assessment topic"},
    }

    def __init__(self):
        self.current_language = "chinese"

    def get_mapping_table(self):
        if self.current_language is "chinese":
            return LanguageMapping.language_mapping_chinese
        elif self.current_language is "english":
            return  LanguageMapping.language_mapping_english


