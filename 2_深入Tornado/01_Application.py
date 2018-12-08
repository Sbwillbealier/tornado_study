#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/6
@file:03options.py
@desc:
"""
import tornado.web
from tornado.web import url
import tornado.ioloop
import tornado.httpserver
import tornado.options
import tornado.httpserver

# 使用config.py的模块中导入config
import config

tornado.options.define('port', default=8000, type=int, help='服务器端口')  # 定义服务器监听的端口选项
tornado.options.define('subjects', default=[], type=str, multiple=True,
                       help='multiple value object.')  # 定义多值项


class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""

    def get(self):
        # self.write('hello itcast')
        self.write('<a href="' + self.reverse_url("python_url") + '">python</a>')


class ItcastHandler(tornado.web.RequestHandler):
    """传字典的路由处理类"""

    def initialize(self, subjects):
        # 对于路由中的字典， 会传入对应的RequestHandler的initialize()方法中
        self.subjects = subjects

    def get(self, *args, **kwargs):
        self.write(self.subjects)


if __name__ == '__main__':
    app = tornado.web.Application([
        ('/', IndexHandler),
        ('/cpp', ItcastHandler, {'subjects': 'C++'}),
        url('/python', ItcastHandler, {'subjects': 'python'}, name='python_url'),
    ], **config.settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()
