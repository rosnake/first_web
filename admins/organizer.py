#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
from handlers.base import BaseHandler
from methods.utils import UserDataUtils
from methods.utils import UserAuthUtils
from methods.debug import *
import json
from methods.controller import PageController
from methods.toolkits import DateToolKits
from orm.organizer import OrganizerModule


# 继承 base.py 中的类 BaseHandler
class AdminOrganizerHandler(BaseHandler):
    """
    用户首页处理，显示一些客户不需要登陆也可查看的信息
    """
    def get(self):
        page_controller = PageController()
        render_controller = page_controller.get_render_controller()
        if self.session["authorized"] is None or self.session["authorized"] is False:
            self.redirect("/login?next=/admin/organizer")
            return

        render_controller["index"] = False
        render_controller["authorized"] = self.session["authorized"]
        render_controller["login"] = False
        render_controller["admin"] = self.session["admin"]
        render_controller["organizer"] = self.session["organizer"]

        username = self.get_current_user()
        if username is not None:
            organizer_tables = self.__get_all_organizer_table()
            self.render("admin/organizer.html",
                        controller=render_controller,
                        username=username,
                        organizer_tables=organizer_tables,
                        )

    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        operation = self.get_argument("operation")
        organizer_name = self.get_argument("organizer_name")
        organizer_id = self.get_argument("organizer_id")
        organizer_date = self.get_argument("time_date")

        logging.info(" organizer_id: " + organizer_id + " organizer_name: "
                      + organizer_name + " organizer_date:" + organizer_date)

        if operation == "delete":
            ret = self.__delete_organizer_by_name(organizer_id)

            if ret is True:
                response["status"] = True
                response["message"] = "删除成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
            else:
                response["status"] = False
                response["message"] = "删除失败！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))

            return

        if operation == "update":
            ret = self.__update_organizer_by_name(organizer_name, organizer_id, organizer_date)
            if ret is True:
                response["status"] = True
                response["message"] = "修改成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
            else:
                response["status"] = False
                response["message"] = "修改失败！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))

            return

    def __get_all_organizer_table(self):
        organizer_module = OrganizerModule.get_all_organizer()
        organizer_table = []

        if organizer_module:
            for x in organizer_module:
                tmp = {"organizer_id": x.organizer, "organizer_name": x.user_name, "date": x.datetime}
                organizer_table.append(tmp)
            return organizer_table
        else:
            return None

    def __delete_organizer_by_name(self, organizer_id):
        organizer = self.db.query(OrganizerModule).filter(OrganizerModule.organizer == organizer_id).first()

        if organizer is not None:
            self.db.delete(organizer)
            self.db.commit()
            logging.info("delete organizer succeed")
            return True
        else:
            logging.error("delete organizer failed")
            return False

    def __update_organizer_by_name(self, organizer_name, organizer_id, organizer_date):
        organizer = self.db.query(OrganizerModule).filter(OrganizerModule.organizer == organizer_id).first()

        if organizer is not None:
            self.db.query(OrganizerModule).filter(OrganizerModule.organizer == organizer_id).update({
                OrganizerModule.user_name: organizer_name,
                OrganizerModule.datetime: organizer_date,
            })
            self.db.commit()
            logging.info("update organizer succeed")
            return True
        else:
            organizer = OrganizerModule()
            organizer.user_name = organizer_name
            organizer.datetime = organizer_date
            organizer.organizer = organizer_id
            organizer.current = True

            self.db.add(organizer)
            self.db.commit()

            return True

