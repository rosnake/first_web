#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from orm.score_criteria import ScoringCriteriaModule
from methods.toolkits import DateToolKits
from methods.debug import *
import json
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth


# 继承 base.py 中的类 BaseHandler
class AdminDisciplineHandler(BaseHandler):
    """
    用于扣分规则管理
    """
    @admin_get_auth("/admin/discipline", True)
    def get(self):
        user_name = self.get_current_user()

        if user_name is not None:
            deduct_tables = self.__get_deduct_tables()
            self.render("admin/discipline.html",
                        deduct_tables=deduct_tables,
                        controller=self.render_controller,
                        user_name=user_name,
                        )

    @admin_post_auth(False)
    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        response["data"] = date_kits.get_now_day_str()

        operation = self.get_argument("operation")
        deduct_name = self.get_argument("deduct_name")
        deduct_id = self.get_argument("id")
        deduct_points = self.get_argument("deduct_points")
        print(type(deduct_points))

        if operation == "add":
            ret = self.__add_deduct(deduct_name, deduct_points)
            if ret is True:
                response["status"] = True
                response["message"] = "新增成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "当前积分规则已存在"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

        if operation == "delete":
            ret = self.__delete_deduct_by_id(deduct_id)
            if ret is True:
                response["status"] = True
                response["message"] = "删除成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "当前积分规则不支持"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

        if operation == "modify":
            ret = self.__modify_deduct_by_id(deduct_id, deduct_points)
            if ret is True:
                response["status"] = True
                response["message"] = "删除成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return
            else:
                response["status"] = False
                response["message"] = "当前用户已存在"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

    def __add_deduct(self, deduct_name, deduct_points):
        discipline = self.db.query(ScoringCriteriaModule).filter(ScoringCriteriaModule.criteria_name == deduct_name).first()
        if discipline is not None:
            logging.error("current is exit")
            return False

        mark = ScoringCriteriaModule()
        mark.criteria_name = deduct_name
        mark.score_value = deduct_points
        self.db.add(mark)
        self.db.commit()
        return True

    def __get_deduct_tables(self):
        deduct_module = ScoringCriteriaModule.get_all_scoring_criteria()
        deduct_tables = []
        if deduct_module:
            for module in deduct_module:
                discipline = {"deduct_id": module.id, "deduct_name": module.criteria_name,
                          "deduct_points": module.score_value}
                deduct_tables.append(discipline)

        return deduct_tables

    def __delete_deduct_by_id(self, deduct_id):
        discipline = self.db.query(ScoringCriteriaModule).filter(ScoringCriteriaModule.id == deduct_id).first()

        if discipline is not None:
            self.db.delete(discipline)
            self.db.commit()
            logging.info("delete discipline succeed")
            return True
        else:
            logging.error("delete discipline failed")
            return False

    def __modify_deduct_by_id(self, deduct_id, deduct_points):
        discipline = self.db.query(ScoringCriteriaModule).filter(ScoringCriteriaModule.id == deduct_id).first()

        if discipline is not None:
            self.db.query(ScoringCriteriaModule).filter(ScoringCriteriaModule.id == deduct_id).update({
                ScoringCriteriaModule.score_value: deduct_points,
            })
            self.db.commit()
            logging.info("modify discipline succeed")
            return True
        else:
            logging.error("modify discipline failed")
            return False
