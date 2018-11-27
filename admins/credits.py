#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
import json
import datetime
from methods.debug import *
from orm.score_info import ScoreInfoModule
from orm.users_info import UsersInfoModule
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth


# 继承 base.py 中的类 BaseHandler
class AdminCreditsHandler(BaseHandler):
    """
    用于积分管理
    """

    @admin_get_auth("/admin/credits", False)
    def get(self):
        user_name = self.get_current_user()
        if user_name is not None:
            self.__update_point_info()
            point_tables = self.__get_all_points()
            if point_tables is not None:
                self.render("admin/credits.html",
                            controller=self.render_controller,
                            user_name=user_name,
                            point_tables=point_tables,
                            language_mapping=self.language_mapping,
                            )

    @admin_post_auth(False)
    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
        user_id = self.get_argument("user_id")
        user_name = self.get_argument("user_name")
        user_point = self.get_argument("user_point")
        purchase_points = self.get_argument("purchase_points", "false")

        logging.info("user post info")
        logging.info("user_id:" + user_id+"user_name:" + user_name+"user_point:" + user_point+
                     " purchase_points:"+purchase_points)
        logging.info(nowTime)
        if user_point.isdigit() is False:
            response["status"] = False
            response["message"] = "输入格式正确，只支持数字"
            response["data"] = nowTime
            self.write(json.dumps(response))
            return

        vip_rechange = False

        if purchase_points == "true":
            vip_rechange = True

        ret = self.__update_user_point_by_user_name(user_id, user_point, vip_rechange)
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
        user_all = UsersInfoModule.get_all_users_info()

        if user_all:
            for x in user_all:
                self.db.query(ScoreInfoModule).filter(ScoreInfoModule.user_name == x.user_name).update({
                    ScoreInfoModule.user_name: x.user_name,
                    ScoreInfoModule.chinese_name: x.chinese_name,
                })
                self.db.commit()

    def __get_all_points(self):
        points_tables = []

        point_module = ScoreInfoModule.get_all_score_info()

        if point_module is None:
            return None

        for point in point_module:
            if point.user_name == "admin":
                continue
            tmp = {"user_id": point.user_name, "user_name": point.chinese_name, "user_point": point.current_scores,
                   "purchase_points": point.purchase_points}
            points_tables.append(tmp)

        return points_tables

    def __update_user_point_by_user_name(self, user_name, point, vip_rechange):
        user_point = self.db.query(ScoreInfoModule).filter(ScoreInfoModule.user_name == user_name).first()

        if user_point:
            self.db.query(ScoreInfoModule).filter(ScoreInfoModule.user_name == user_name).update({
                ScoreInfoModule.last_scores: user_point.current_scores,
                ScoreInfoModule.current_scores: point,
                ScoreInfoModule.purchase_points: vip_rechange,
            })
            self.db.commit()
            return True
        else:
            return False
