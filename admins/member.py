#!/usr/bin/env Python
# coding=utf-8

import json
from handlers.base import BaseHandler
from orm.users_info import UsersInfoModule
from orm.score_info import ScoreInfoModule
from methods.debug import *
from methods.toolkits import DateToolKits
import random
import string
from admins.decorator import admin_get_auth
from admins.decorator import admin_post_auth


# 继承 base.py 中的类 BaseHandler
class AdminMemberHandler(BaseHandler):
    """
    用于人员管理
    """

    @admin_get_auth("/admin/member", True)
    def get(self):
        user_name = self.get_current_user()
        if user_name is not None:
            user_tables = self.__get_all_user_info()
            self.render("admin/member.html", user_tables=user_tables,
                        controller=self.render_controller, user_name=user_name)

    @admin_post_auth(False)
    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        operation = self.get_argument("operation")
        user_name = self.get_argument("user_name")
        uid = self.get_argument("id")
        user_role = self.get_argument("role")

        logging.info("operation:%s , user_name: %s, role:%s id: %s" % (operation, user_name, role, uid))

        if uid.isdigit() is False:
            response["status"] = False
            response["message"] = "id只支持数字！"
            response["data"] = date_kits.get_now_day_str()
            self.write(json.dumps(response))
            return

        str_tmp = uid.encode("ascii")
        user_id = int(str_tmp)

        auth = self.__auth_check_by_user_name(self.session["user_name"])
        if auth is False:
            response["status"] = False
            response["message"] = "您无权限操作！"
            response["data"] = date_kits.get_now_day_str()
            self.write(json.dumps(response))

            return

        if operation == "delete":
            ret = self.__delete_user_by_name(user_name)

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

            self.__delete_point_by_name(user_name)
            return

        if operation == "modify":
            ret = self.__modify_user_info_by_id(user_id, user_name, user_role)
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

        if operation == "add":
            ret = self.__add_user(user_name, user_role)
            if ret is True:
                response["status"] = True
                response["message"] = "新增成功！"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
            else:
                response["status"] = False
                response["message"] = "当前用户已存在"
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

        if operation == "show_pwd":
            ret, pass_word = self.__show_user_pass_word(user_name)
            if ret is True:
                response["status"] = True
                response["message"] = pass_word
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
            else:
                response["status"] = False
                response["message"] = pass_word
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

    def __show_user_pass_word(self, user_name):
        user = self.db.query(UsersInfoModule).filter(UsersInfoModule.user_name == user_name).first()

        if user is not None:
            if user.pwd_modified is False:
                pass_word = user.pass_word
                return True, pass_word
            else:
                pass_word = "用户已修改密码，无法查看"
                return True, pass_word
        else:
            logging.error("modify user failed")
            pass_word = "用户不存在"
            return False, pass_word

    def __delete_point_by_name(self, user_name):
        point = self.db.query(ScoreInfoModule).filter(ScoreInfoModule.user_name == user_name).first()

        if point is not None:
            self.db.delete(point)
            self.db.commit()
            logging.info("delete point succeed")
            return True
        else:
            logging.error("delete point failed")
            return False

    def __get_all_user_info(self):
        user_tables = []
        user_all = self.db.query(UsersInfoModule).all()
        if user_all is not None:
            for x in user_all:
                uses = {"id": x.id, "user_name": x.user_name, "passwd": x.pass_word, "role": x.user_role}
                user_tables.append(uses)

        return user_tables

    def __delete_user_by_name(self, user_name):
        user = self.db.query(UsersInfoModule).filter(UsersInfoModule.user_name == user_name).first()

        if user is not None:
            self.db.delete(user)
            self.db.commit()
            logging.info("delete user succeed")
            return True
        else:
            logging.error("delete user failed")
            return False

    def __auth_check_by_user_name(self, user_name):
        logging.info("check auto user_name:"+user_name)
        user = self.db.query(UsersInfoModule).filter(UsersInfoModule.user_name == user_name).first()

        if user is not None:
            logging.info("current user is not none")
            if user.user_role == "admin":
                logging.info("current user user_role is admin")
                return True
            else:
                logging.info("current user user_role is not  admin")
                return False
        else:
            logging.info("current user is none")
            return False

    def __modify_user_info_by_id(self, user_id, user_name, user_role):
        user = self.db.query(UsersInfoModule).filter(UsersInfoModule.id == user_id).first()

        if user is not None:
            self.db.query(UsersInfoModule).filter(UsersInfoModule.id == user_id).update({
                UsersInfoModule.user_name: user_name,
                UsersInfoModule.user_user_role: user_role,
            })
            self.db.commit()
            logging.info("modify user succeed")
            return True
        else:
            logging.error("modify user failed")
            return False

    def __add_user(self, user_name, user_role):

        user = self.db.query(UsersInfoModule).filter(UsersInfoModule.user_name == user_name).first()
        if user is not None:
            logging.error("current is exit")
            return False

        pass_word = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        user_moudle = UsersInfoModule()
        user_moudle.user_name = user_name
        user_moudle.pass_word = pass_word
        user_moudle.nick_name = "unknown"
        user_moudle.address = "unknown"
        user_moudle.department = "unknown"
        user_moudle.email = "unknown"
        user_moudle.user_role = user_role

        self.db.add(user_moudle)
        self.db.commit()

        # 更新积分表格
        point_moudle = ScoreInfoModule()
        point_moudle.user_name = user_name
        point_moudle.current_point = 10
        point_moudle.last_point = 10
        point_moudle.nick_name = user_moudle.nick_name
        self.db.add(point_moudle)
        self.db.commit()

        return True





