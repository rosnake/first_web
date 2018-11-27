#!/usr/bin/env Python
# coding=utf-8
from config.debug import DebugConfig
import logging  # 引入logging模块
# logging.basicConfig函数对日志的输出格式及方式做相关配置
if DebugConfig.DEBUG is False:
    logging.basicConfig(level=logging.DEBUG,
                        #  控制台打印的日志级别
                        filename='web.log',
                        #  模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                        filemode='a',
                        # a是追加模式，默认如果不写的话，就是追加模式
                        format='%(asctime)s - %(funcName)s-%(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
else:
    logging.basicConfig(level=logging.DEBUG,
                        #  控制台打印的日志级别
                        format='%(asctime)s - %(funcName)s-%(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

def debug_msg(cls,line, msg):
    print("["+cls.__name__+" "+str(line)+" ]:"+msg)