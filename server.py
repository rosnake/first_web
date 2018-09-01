#!/usr/bin/env Python
# coding=utf-8

import tornado.ioloop
import tornado.options
import tornado.httpserver

from application import application
from orm.create_tables import *

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)
define("tables", default=False, group="application", help="create tables", type=bool)

def main():
    tornado.options.parse_command_line()
    tornado.options.parse_command_line()
    if options.tables:
        create_all_tables()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    print("Development server is running at http://127.0.0.1:%s" % options.port)
    print("Quit the server with Control-C")
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
