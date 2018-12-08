#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/6
@file:02httpserver-多进程启动.py
@desc:
"""
import tornado.web
import tornado.ioloop
import tornado.httpserver


# 2.定义实现路由映射表中的handler类
class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""

    def get(self, *args, **kwargs):
        self.write('hello itcast')


if __name__ == '__main__':
    # 1.创建web应用实例
    app = tornado.web.Application([
        ('/', IndexHandler),
    ])

    # 3.创建一个http服务器并绑定端口
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    http_server.start(1)

    # 4.启动当前线程的IOLoop,循环查询epoll有无新的socket要处理
    tornado.ioloop.IOLoop.current().start()
