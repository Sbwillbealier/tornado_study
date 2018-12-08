#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/7
@file:04_status_redirect.py
@desc:
"""
import json
from tornado.web import Application, RequestHandler
import tornado.ioloop
import tornado.httpserver


class IndexHandler(RequestHandler):

    def set_default_headers(self):
        print('执行力set_default_header()')
        self.set_header('Content-Type', 'application/json; charset=utf-8')

    def get(self):
        # 多个write会把响应内容写到缓冲区，最终一并作为本次请求的响应
        # self.write('hello tornado 1<br>')
        # self.write('hello tornado 2<br>')
        # self.write('hello tornado 3<br>')

        # json数据
        stu = {
            "name": "tornado学习",
            "age": 10,
            "gender": 1,
        }
        # 手动序列化json, Content-Type: text/plain
        # stu_json = json.dumps(stu)
        # print(type(stu_json))
        # self.write(stu_json)

        # 非手动序列化json, Content-Type: application/json; charset=UTF-8
        self.write(stu)

        # set_header
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

    def post(self):
        stu = {
            "name": "tornado学习",
            "age": 10,
            "gender": 1,
        }
        stu_json = json.dumps(stu)
        self.write(stu_json)


class LoginHandler(RequestHandler):
    """对应 /login"""

    def get(self):
        self.write('<form method="POST"><input type="submit" value="登录"></form>')

    def post(self):
        self.redirect('/')


class Err404Handler(RequestHandler):
    """对应 /err/404"""

    def get(self):
        self.write("hello tornado")
        self.set_status(404)  # 标准状态码，可省略reason


class Err211Handler(RequestHandler):
    """对应 /err/404"""

    def get(self):
        self.write("hello tornado")
        self.set_status(211, reason='tornado error')  # 非标准状态码，不可省略reason. Status Code: 211 tornado error


if __name__ == '__main__':
    app = Application([
        ('/', IndexHandler),
        ('/login', LoginHandler),
        ('/err/404', Err404Handler),
        ('/err/211', Err211Handler),
    ], debug=True)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)

    tornado.ioloop.IOLoop.current().start()
