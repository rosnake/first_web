#!/usr/bin/env Python
# coding=utf-8

#该文件用于通用数据接口

class UserDataUtils:

    user_score_tables = [
        {"name": "raoyuanqin", "late": -1, "retreat": 0, "absenteeism": 0, "un_present": 0, "total": 10},
        {"name": "chenmeijing", "late": -1, "retreat": 0, "absenteeism": 0, "un_present": 0, "total": 11},
        {"name": "chenxiaojie", "late": -1, "retreat": 0, "absenteeism": -1, "un_present": 0, "total": 9},
        {"name": "raoxiansheng", "late": -1, "retreat": -1, "absenteeism": 0, "un_present": 0, "total": 12},
    ]
    user_info_tables = [
        {
            "name": "chenhaha",
            "image": "images/chenhaha.jpg",
            "remnants": 11,
            "sub": -8,
            "add": 12,
            "description": "<p>这世界要是没有爱情，它在我们心中还会有什么意义！这就如一盏没有亮光的走马灯</p>"
        },
        {
            "name": "raohaha",
            "image": "images/raohaha.jpg",
            "remnants": 10,
            "sub": -9,
            "add": 15,
            "description": "<p>菩提本无树，明镜亦非台</p>"
        }
    ]
    user_table = [
        {"name": "raoyuanqin", "passwd": "123456"},
        {"name": "chenmeijing", "passwd": "123456"},
        {"name": "chenxiaojie", "passwd": "123456"},
        {"name": "raoxiansheng", "passwd": "123456"},
    ]
    render_controller = {"index": False, "authorized": True, "login":False,"admin":False}

    user_topics_tables = [
        {
            "name": "chenmeijing",
            "image": "images/chenhaha.jpg",
            "title":"读书分享",
            "current":True,
            "time":"2018-8-6",
            "description": "<p>这世界要是没有爱情，它在我们心中还会有什么意义！这就如一盏没有亮光的走马灯</p>"
        },
        {
            "name": "raoyuanqin",
            "image": "images/raohaha.jpg",
            "title":"读书分享2",
            "current": False,
            "time": "2018-7-26",
            "description": "<p>菩提本无树，明镜亦非台</p>"
        }
    ]

    def __init__(self):
        pass

    @staticmethod
    def login_check(username, passwd):
        for user in UserDataUtils.user_table:
            if user["name"] == username and user["passwd"] == passwd:
                return True

        return  False

    @staticmethod
    def get_user_score_tables():
        return  UserDataUtils.user_score_tables

    @staticmethod
    def get_user_info_tables():
        return UserDataUtils.user_info_tables

    @staticmethod
    def get_user_info_by_name(username):
        for user_info in UserDataUtils.user_info_tables:

            if user_info["name"] == username:
                return user_info

        return None

    @staticmethod
    def get_user_score_by_name(username):
        for user_score in UserDataUtils.user_score_tables:
            print("name:"+ user_score["name"])
            if user_score["name"] == username:
                print("=====name:" + user_score["name"])
                return user_score

        return None

    @staticmethod
    def get_render_controller():
        return UserDataUtils.render_controller

    @staticmethod
    def get_user_topics_table():
        return UserDataUtils.user_topics_tables

    @staticmethod
    def get_user_topics_by_name(username):
        for user_topic in UserDataUtils.user_topics_tables:

            if user_topic["name"] == username:
                return user_topic

        return None


class UserAuthUtils:
    user_infos=[
        {"username": "raoyuanqin", "passwd": "123456", "role":"admin"},
        {"username": "chenmeijing", "passwd": "123456","role":"normal"},
        {"username": "chenxiaojie", "passwd": "123456","role":"normal"},
        {"username": "raoxiansheng", "passwd": "123456","role":"normal"},
    ]
    verify_code=""

    def __init__(self):
        pass
    """
    用户验证，存在用户返回True，不存在返回False
    """
    @staticmethod
    def authenticate_user_by_name(username, passwd):
        for user_info in UserAuthUtils.user_infos:
            if user_info["username"] == username and  user_info["passwd"] == passwd:
                return True

        return  False

    @staticmethod
    def get_role_by_name(username):
        for user_info in UserAuthUtils.user_infos:
            if user_info["username"] == username:
                return user_info["role"]

        return  None

    @staticmethod
    def get_verify_code():
        return UserAuthUtils.verify_code

    @staticmethod
    def set_verify_code(verify_code):
        UserAuthUtils.verify_code = verify_code