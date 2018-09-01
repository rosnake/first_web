#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from handlers.base import BaseHandler
from methods.utils import UserDataUtils
from methods.utils import UserAuthUtils
from orm.marks import MarksModule
from methods.controller import PageController  # 导入页面控制器
from methods.toolkits import DateToolKits
from methods.debug import *
import json


# 继承 base.py 中的类 BaseHandler
class AdminDeductHandler(BaseHandler):
    """
    用户首页处理，显示一些客户不需要登陆也可查看的信息
    """
    def get(self):
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()
        if self.session["authorized"] is None or self.session["authorized"] is False:
            self.redirect("/login")
            return

        username = self.get_current_user()

        render_controller["index"] = True
        render_controller["authorized"] = False
        render_controller["login"] = False
        render_controller["authorized"] = self.session["authorized"]

        if username is not None:
            deduct_module = MarksModule.get_all_marks()
            deduct_tables = []
            self.__convent_module_to_table(deduct_module, deduct_tables)
            self.render("admin/deduct.html",
                        deduct_tables=deduct_tables,
                        controller=render_controller,
                        username=username,
                        )

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
        deduct = self.db.query(MarksModule).filter(MarksModule.markname == deduct_name).first()
        if deduct is not None:
            logging.error("current is exit")
            return False

        mark = MarksModule()
        mark.markname = deduct_name
        mark.points = deduct_points
        self.db.add(mark)
        self.db.commit()
        return True

    def __convent_module_to_table(self, deduct_module, deduct_tables):
        if deduct_module is None:
            return False

        for module in deduct_module:
            deduct = {"deduct_id": module.id, "deduct_name": module.markname, "deduct_points": module.points}
            deduct_tables.append(deduct)

        return True

    def __delete_deduct_by_id(self, deduct_id):
        deduct = self.db.query(MarksModule).filter(MarksModule.id == deduct_id).first()

        if deduct is not None:
            self.db.delete(deduct)
            self.db.commit()
            logging.info("delete deduct succeed")
            return True
        else:
            logging.error("delete deduct failed")
            return False

    def __modify_deduct_by_id(self, deduct_id, deduct_points):
        deduct = self.db.query(MarksModule).filter(MarksModule.id == deduct_id).first()

        if deduct is not None:
            self.db.query(MarksModule).filter(MarksModule.id == deduct_id).update({
                MarksModule.points: deduct_points,
            })
            self.db.commit()
            logging.info("modify deduct succeed")
            return True
        else:
            logging.error("modify deduct failed")
            return False
