#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/6
@file:03options.py
@desc:
    tornado.options: 全局参数定义、存储、转换
    tornado.options.define(): 用来定义选项的方法
    tornado.options.options: 全局options对象，包含所有的选项变量
    tornado.options.parse_command_line(): 解析命令行参数，并将值设置到全局options对象相关属性上
    tornado.options.parse_config_file(path): 导入配置文件

"""
import tornado.web
from tornado.web import url
import tornado.ioloop
import tornado.httpserver
import tornado.options
import tornado.httpserver

tornado.options.define('port', default=8000, type=int, help='run server on given port.')  # 定义服务器监听的端口选项
tornado.options.define('subjects', default=[], type=str, multiple=True,
                       help='multiple value object.')  # 定义多值项


class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""

    def get(self, *args, **kwargs):
        self.write('hello itcast')


class ItcastHandler(tornado.web.RequestHandler):
    """传字典的路由处理类"""

    def initialize(self, subjects):
        # 对于路由中的字典， 会传入对应的RequestHandler的initialize()方法中
        self.subjects = subjects

    def get(self, *args, **kwargs):
        self.write(self.subjects)


if __name__ == '__main__':
    # 关闭默认日志功能
    # tornado.options.options.logging = None

    # 命令行启动并查看变量信息
    # tornado.options.parse_command_line()

    # 从配置文件中导入option
    tornado.options.parse_config_file('./03config')

    print(tornado.options.options.subjects)

    app = tornado.web.Application([
        ('/', IndexHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()
