#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from handlers.base import BaseHandler
from methods.utils import UserDataUtils
from methods.utils import UserAuthUtils
import json
import datetime
from methods.debug import *
from methods.controller import PageController
from orm.points import PointsModule
from orm.user import UserModule


# 继承 base.py 中的类 BaseHandler
class AdminPointHandler(BaseHandler):
    """
    用户首页处理，显示一些客户不需要登陆也可查看的信息
    """
    def get(self):
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()
        if self.session["authorized"] is None or self.session["authorized"] is False:
            self.redirect("/login?next=/admin/point")
            return

        username = self.get_current_user()
        if username is None:
            self.redirect("/login?next=/admin/point")
            return

        print(self.session["authorized"])
        render_controller["index"] = False
        render_controller["authorized"] = self.session["authorized"]
        render_controller["login"] = False
        render_controller["admin"] = self.session["admin"]
        render_controller["organizer"] = self.session["organizer"]
        self.__update_point_info()
        point_tables = self.__get_all_points()
        if point_tables is not None:
            self.render("admin/point.html",
                        controller=render_controller,
                        username=username,
                        point_tables=point_tables,
                        )

    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
        user_id = self.get_argument("user_id")
        user_name = self.get_argument("user_name")
        user_point = self.get_argument("user_point")

        logging.info("user post info")
        logging.info("user_id:" + user_id+"user_name:" + user_name+"user_point:" + user_point)
        logging.info(nowTime)
        if user_point.isdigit() is False:
            response["status"] = False
            response["message"] = "输入格式正确，只支持数字"
            response["data"] = nowTime
            self.write(json.dumps(response))
            return

        ret = self.__update_user_point_by_username(user_id, user_point)
        if ret is True:
            response["status"] = True
            response["message"] = "修改成功！"
            response["data"] = nowTime
            self.write(json.dumps(response))
            return
        else:
            response["status"] = False
            response["message"] = "修改失败,找不到记录！"
            response["data"] = nowTime
            self.write(json.dumps(response))
            return

    def __update_point_info(self):
        user_all = UserModule.get_all_users()

        if user_all:
            for x in user_all:
                self.db.query(PointsModule).filter(PointsModule.username == x.username).update({
                    PointsModule.username: x.username,
                    PointsModule.nickname: x.nickname,
                })
                self.db.commit()

    def __get_all_points(self):
        points_tables = []

        point_module = PointsModule.get_all_points()

        if point_module is None:
            return None

        for point in point_module:
            tmp = {"user_id": point.username, "user_name": point.nickname, "user_point": point.current_point}
            points_tables.append(tmp)

        return points_tables

    def __update_user_point_by_username(self, username, point):
        user_point = self.db.query(PointsModule).filter(PointsModule.username == username).first()

        if user_point:
            self.db.query(PointsModule).filter(PointsModule.username == username).update({
                PointsModule.last_point:user_point.current_point,
                PointsModule.current_point: point,
            })
            self.db.commit()
            return True
        else:
            return False
