#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/7
@file:05_error.py
@desc:
"""

import json
from tornado.web import Application, RequestHandler
import tornado.ioloop
import tornado.httpserver


class IndexHandler(RequestHandler):

    def write_error(self, status_code, **kwargs):
        # 默认的write_error不会处理send_error抛出来的kwargs
        self.write('status_code: {} <br>'.format(status_code))
        self.write('title: {} <br>'.format(kwargs.get('err_title')))
        self.write('content: {} <br>'.format(kwargs.get('err_content')))

    def get(self):
        # 使用send_error抛出的错误后tornado会调用write_error()方法处理
        err_content = {
            'err_title': '页面丢失！',
            'err_content': '您访问的页面不存在！',
        }

        self.send_error(status_code=404, **err_content)

        # send_error后面的write不会再写入缓冲区，无效
        # self.write('index')

    def post(self):
        stu = {
            "name": "tornado学习",
            "age": 10,
            "gender": 1,
        }
        stu_json = json.dumps(stu)
        self.write(stu_json)


if __name__ == '__main__':
    app = Application([
        ('/', IndexHandler),
    ], debug=True)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)

    tornado.ioloop.IOLoop.current().start()
