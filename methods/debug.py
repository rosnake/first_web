#!/usr/bin/env Python
# coding=utf-8

from db import *
import sys

def debug_msg(cls,line, msg):
    print("["+cls.__name__+" "+str(line)+" ]:"+msg)