#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/6
@file:01hello.py
@desc:
"""
import tornado.web
import tornado.ioloop


# 2.定义实现路由映射表中的handler类
class IndexHandler(tornado.web.RequestHandler):
    """主页路由类"""

    def post(self):
        """对应http的get请求方式"""
        self.write('hello tornado!')


if __name__ == '__main__':
    # 1.创建web应用实例，是与服务器对接的接口，第一个参数为路由映射表
    app = tornado.web.Application([
        (r'/', IndexHandler),
    ])

    # 3.创建一个http服务器并绑定端口
    app.listen(8000)

    # 4.启动当前线程的IOLoop,循环查询epoll有无新的socket要处理
    tornado.ioloop.IOLoop.current().start()
