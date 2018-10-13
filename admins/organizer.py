#!/usr/bin/env Python
# coding=utf-8

from handlers.base import BaseHandler
from methods.debug import *
import json
from methods.toolkits import DateToolKits
from orm.organizer_info import OrganizerInfoModule
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth
from orm.users_info import UsersInfoModule


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
            user_tables = self.__get_all_user_table()
            self.render("admin/organizer.html",
                        controller=self.render_controller,
                        user_name=user_name,
                        organizer_tables=organizer_tables,
                        language_mapping=self.language_mapping,
                        user_tables=user_tables,
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

        if operation == "assign":
            ret = self.__assign_organizer_by_name(organizer_name, organizer_id, organizer_date)
            if ret is True:
                response["status"] = True
                response["message"] = "指定成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
            else:
                response["status"] = False
                response["message"] = "指定失败！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))

            return

    def __get_all_organizer_table(self):
        organizer_module = OrganizerInfoModule.get_all_organizer_info()
        organizer_table = []

        if organizer_module:
            for organizer in organizer_module:
                tmp = {"organizer_id": organizer.user_name, "organizer_name": organizer.chinese_name,
                       "date": organizer.date_time, "current": organizer.current}
                organizer_table.append(tmp)
            return organizer_table
        else:
            return None

    def __get_all_user_table(self):
        user_module = UsersInfoModule.get_all_users_info()
        user_table = []

        if user_module:
            for user in user_module:
                if user.user_role != "root":

                    tmp = {"user_id": user.id, "user_name": user.user_name, "chinese_name": user.chinese_name}
                    user_table.append(tmp)

            return user_table
        else:
            return None

    def __assign_organizer_by_name(self, organizer_name, organizer_id, organizer_date):
        # 1.更新其他组织者为非当前
        organizer_module = OrganizerInfoModule.get_all_organizer_info()
        if organizer_module:
            for organizer in organizer_module:
                if organizer.current is True:
                    self.db.query(OrganizerInfoModule).filter(OrganizerInfoModule.user_name == organizer.user_name).update({
                        OrganizerInfoModule.current: False,
                    })
                    self.db.commit()

        # 2.更新当前组织者表格
        organizer = self.db.query(OrganizerInfoModule).filter(OrganizerInfoModule.user_name == organizer_id).first()

        if organizer is not None:
            self.db.query(OrganizerInfoModule).filter(OrganizerInfoModule.user_name == organizer_id).update({
                OrganizerInfoModule.chinese_name: organizer_name,
                OrganizerInfoModule.date_time: organizer_date,
                OrganizerInfoModule.current: True,
            })
            self.db.commit()
            logging.info("update organizer succeed")
            return True
        else:
            organizer = OrganizerInfoModule()
            organizer.chinese_name = organizer_name
            organizer.date_time = organizer_date
            organizer.user_name = organizer_id
            organizer.current = True

            self.db.add(organizer)
            self.db.commit()

            return True

