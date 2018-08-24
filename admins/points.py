#!/usr/bin/env Python
# coding=utf-8

import tornado.escape
import methods.readdb as mrd
from handlers.base import BaseHandler
from methods.utils import UserDataUtils
from methods.utils import UserAuthUtils
import json
import datetime

import logging  # 引入logging模块
# logging.basicConfig函数对日志的输出格式及方式做相关配置
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(funcName)s-%(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

# 继承 base.py 中的类 BaseHandler
class AdminPointHandler(BaseHandler):
    """
    用户首页处理，显示一些客户不需要登陆也可查看的信息
    """
    def get(self):
        usernames = mrd.select_columns(table="users",column="username")
        one_user = usernames[0][0]
        # print ("one user name:%s" % one_user)
        username = self.get_current_user()
        controller = UserDataUtils.get_render_controller()
        controller["index"] = True
        controller["authorized"] = False
        controller["login"] = False
        score_tables = UserDataUtils.get_user_score_tables()

        if username is not None:
            controller["authorized"] = True
            print("################"+username)

        point_tables = UserDataUtils.get_point_tables()
        persons = UserDataUtils.get_user_info_tables()
        self.render("admin_point.html",
                    persons = persons,
                    controller = controller,
                    username=username,
                    point_tables=point_tables,
                    )

    def post(self):
        response = {"status": True, "data": "", "message": "succeed"}
        user_id = self.get_argument("user_id")
        user_name = self.get_argument("user_name")
        user_point = self.get_argument("user_point")

        logging.info("user post info")
        logging.info("user_id:" + user_id)
        logging.info("user_name:" + user_name)
        logging.info("user_point:" + user_point)

        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
        logging.info(nowTime)
        if user_point.isdigit() is False:
            response["status"] = False
            response["message"] = "输入格式正确，只支持数字"
            response["data"] = nowTime
            self.write(json.dumps(response))
            return

        ret = UserDataUtils.set_point_to_tables_by_id(user_id, user_point)
        if ret is True:
            response["status"] = True
            response["message"] = "修改成功！"
            response["data"] = nowTime
            self.write(json.dumps(response))
            return

        response["status"] = False
        response["message"] = "修改失败,找不到记录！"
        response["data"] = nowTime
        self.write(json.dumps(response))
        return


