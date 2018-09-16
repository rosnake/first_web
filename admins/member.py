#!/usr/bin/env Python
# coding=utf-8

import json
from handlers.base import BaseHandler
from orm.user import UserModule
from orm.points import PointsModule
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
        username = self.get_current_user()
        if username is not None:
            user_tables = self.__get_all_user_info()
            self.render("admin/member.html", user_tables=user_tables,
                        controller=self.render_controller, username=username)

    @admin_post_auth(False)
    def post(self):
        response = {"status": True, "data": "", "message": "failed"}
        date_kits = DateToolKits()
        operation = self.get_argument("operation")
        username = self.get_argument("username")
        uid = self.get_argument("id")
        role = self.get_argument("role")

        logging.info("operation:%s , username: %s, role:%s id: %s" % (operation, username, role, uid))

        if uid.isdigit() is False:
            response["status"] = False
            response["message"] = "id只支持数字！"
            response["data"] = date_kits.get_now_day_str()
            self.write(json.dumps(response))
            return

        str_tmp = uid.encode("ascii")
        user_id = int(str_tmp)

        auth = self.__auth_check_by_username(self.session["username"])
        if auth is False:
            response["status"] = False
            response["message"] = "您无权限操作！"
            response["data"] = date_kits.get_now_day_str()
            self.write(json.dumps(response))

            return

        if operation == "delete":
            ret = self.__delete_user_by_name(username)

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

            self.__delete_point_by_name(username)
            return

        if operation == "modify":
            ret = self.__modify_user_info_by_id(user_id, username, role)
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
            ret = self.__add_user(username, role)
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
            ret, password = self.__show_user_password(username)
            if ret is True:
                response["status"] = True
                response["message"] = password
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
            else:
                response["status"] = False
                response["message"] = password
                response["data"] = date_kits.get_now_day_str()
                self.write(json.dumps(response))
                return

    def __show_user_password(self, username):
        user = self.db.query(UserModule).filter(UserModule.username == username).first()

        if user is not None:
            if user.pwd_modified is False:
                password = user.password
                return True, password
            else:
                password = "用户已修改密码，无法查看"
                return True, password
        else:
            logging.error("modify user failed")
            password = "用户不存在"
            return False, password

    def __delete_point_by_name(self, username):
        point = self.db.query(PointsModule).filter(PointsModule.username == username).first()

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
        user_all = self.db.query(UserModule).all()
        if user_all is not None:
            for x in user_all:
                uses = {"id": x.id, "username": x.username, "passwd": x.password, "role": x.role}
                user_tables.append(uses)

        return user_tables

    def __delete_user_by_name(self, username):
        user = self.db.query(UserModule).filter(UserModule.username == username).first()

        if user is not None:
            self.db.delete(user)
            self.db.commit()
            logging.info("delete user succeed")
            return True
        else:
            logging.error("delete user failed")
            return False

    def __auth_check_by_username(self, username):
        logging.info("check auto username:"+username)
        user = self.db.query(UserModule).filter(UserModule.username == username).first()

        if user is not None:
            logging.info("current user is not none")
            if user.role == "admin":
                logging.info("current user role is admin")
                return True
            else:
                logging.info("current user role is not  admin")
                return False
        else:
            logging.info("current user is none")
            return False

    def __modify_user_info_by_id(self, user_id, username, role):
        user = self.db.query(UserModule).filter(UserModule.id == user_id).first()

        if user is not None:
            self.db.query(UserModule).filter(UserModule.id == user_id).update({
                UserModule.username: username,
                UserModule.role: role,
            })
            self.db.commit()
            logging.info("modify user succeed")
            return True
        else:
            logging.error("modify user failed")
            return False

    def __add_user(self, username, role):

        user = self.db.query(UserModule).filter(UserModule.username == username).first()
        if user is not None:
            logging.error("current is exit")
            return False

        password = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        user_moudle = UserModule()
        user_moudle.username = username
        user_moudle.password = password
        user_moudle.nickname = "unknown"
        user_moudle.address = "unknown"
        user_moudle.department = "unknown"
        user_moudle.email = "unknown"
        user_moudle.role = role

        self.db.add(user_moudle)
        self.db.commit()

        # 更新积分表格
        point_moudle = PointsModule()
        point_moudle.username = username
        point_moudle.current_point = 10
        point_moudle.last_point = 10
        point_moudle.nickname = user_moudle.nickname
        self.db.add(point_moudle)
        self.db.commit()

        return True





