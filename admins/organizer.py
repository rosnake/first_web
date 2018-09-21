#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from methods.debug import *
import json
from methods.toolkits import DateToolKits
from orm.organizer_info import OrganizerInfoModule
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth


# 继承 base.py 中的类 BaseHandler
class AdminOrganizerHandler(BaseHandler):
    """
    用于组织者管理
    """
    @admin_get_auth("/admin/organizer", False)
    def get(self):
        user_name = self.get_current_user()
        if user_name is not None:
            organizer_tables = self.__get_all_organizer_table()
            self.render("admin/organizer.html",
                        controller=self.render_controller,
                        user_name=user_name,
                        organizer_tables=organizer_tables,
                        language_mapping=self.language_mapping,
                        )

    @admin_post_auth(False)
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
        organizer_module = OrganizerInfoModule.get_all_organizer_info()
        organizer_table = []

        if organizer_module:
            for x in organizer_module:
                tmp = {"organizer_id": x.organizer, "organizer_name": x.user_name, "date": x.datetime}
                organizer_table.append(tmp)
            return organizer_table
        else:
            return None

    def __delete_organizer_by_name(self, organizer_id):
        organizer = self.db.query(OrganizerInfoModule).filter(OrganizerInfoModule.user_name == organizer_id).first()

        if organizer is not None:
            self.db.delete(organizer)
            self.db.commit()
            logging.info("delete organizer succeed")
            return True
        else:
            logging.error("delete organizer failed")
            return False

    def __update_organizer_by_name(self, organizer_name, organizer_id, organizer_date):
        organizer = self.db.query(OrganizerInfoModule).filter(OrganizerInfoModule.user_name == organizer_id).first()

        if organizer is not None:
            self.db.query(OrganizerInfoModule).filter(OrganizerInfoModule.user_name == organizer_id).update({
                OrganizerInfoModule.user_name: organizer_name,
                OrganizerInfoModule.date_time: organizer_date,
            })
            self.db.commit()
            logging.info("update organizer succeed")
            return True
        else:
            organizer = OrganizerInfoModule()
            organizer.chinese_name = organizer_name
            organizer.datetime = organizer_date
            organizer.organizer = organizer_id
            organizer.current = True

            self.db.add(organizer)
            self.db.commit()

            return True

