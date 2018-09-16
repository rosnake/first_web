#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
import json
import datetime
from methods.debug import *
from orm.points import PointsModule
from orm.user import UserModule
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth


# 继承 base.py 中的类 BaseHandler
class AdminPointHandler(BaseHandler):
    """
    用于积分管理
    """

    @admin_get_auth("/admin/point", False)
    def get(self):
        username = self.get_current_user()
        if username is not None:
            self.__update_point_info()
            point_tables = self.__get_all_points()
            if point_tables is not None:
                self.render("admin/point.html",
                            controller=self.render_controller,
                            username=username,
                            point_tables=point_tables,
                            )

    @admin_post_auth(False)
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
                PointsModule.last_point: user_point.current_point,
                PointsModule.current_point: point,
            })
            self.db.commit()
            return True
        else:
            return False
