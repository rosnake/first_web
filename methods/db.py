#!/usr/bin/env Python
# coding=utf-8

import MySQLdb
#!/usr/bin/env Python
# coding=utf-8

import MySQLdb

conn = MySQLdb.connect(host="localhost", user="root", passwd="tornado123", db="tornadotest", port=3306, charset="utf8")    #连接对象

cur = conn.cursor()    #游标对象
