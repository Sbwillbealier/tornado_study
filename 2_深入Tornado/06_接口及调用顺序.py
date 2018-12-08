#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/7
@file:06_接口及调用顺序.py
@desc:
"""
import json
from tornado.web import Application, RequestHandler
import tornado.ioloop
import tornado.httpserver


class IndexHandler(RequestHandler):
    def initialize(self):
        print('initialize')

    def prepare(self):
        print('prepare')

    def set_default_headers(self):
        print('set_default_headers')

    def write_error(self, status_code, **kwargs):
        print('write_error')

    def get(self):
        print('get')

    def post(self):
        print('post')
        self.send_error(status_code=300)

    def on_finish(self):
        print('on_finish')


if __name__ == '__main__':
    app = Application([
        ('/', IndexHandler),
    ], debug=True)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)

    tornado.ioloop.IOLoop.current().start()
