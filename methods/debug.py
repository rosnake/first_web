#!/usr/bin/env Python
# coding=utf-8

import logging  # 引入logging模块
# logging.basicConfig函数对日志的输出格式及方式做相关配置
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(funcName)s-%(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

def debug_msg(cls,line, msg):
    print("["+cls.__name__+" "+str(line)+" ]:"+msg)