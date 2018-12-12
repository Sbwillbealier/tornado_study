#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/12
@file:07_并行协程.py
@desc:
"""
import os
import tornado.web
import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.httpclient
import tornado.websocket
import datetime


class IndexHandler(tornado.web.RequestHandler):
    """首页handler类"""

    def get(self):
        self.render('index.html')


class ChatHandler(tornado.websocket.WebSocketHandler):
    """websocket处理类"""

    users = []

    def open(self):
        """WebSocke连接建立"""
        self.users.append(self)  # 把当前对象添加进去
        for u in self.users:
            u.write_message(
                '[{}]-[{}]-进入聊天室'.format(self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def on_message(self, message):
        """接收到消息"""
        # 向在线用户发消息
        for u in self.users:
            u.write_message("[{}]-[{}]-说：{}".format(self.request.remote_ip,
                                                    datetime.datetime.now().strftime("%Y-%m%d %H:%M:%S"),
                                                    message
                                                    ))

    def on_close(self):
        self.users.remove(self)  # 将用户移除容器
        for u in self.users:
            u.write_message(
                "[{}]-[{}]-离开聊天室".format(self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m%d %H:%M:%S")))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求


class Application(tornado.web.Application):
    """应用对象类"""

    def __init__(self):
        handlers = [
            ('/', IndexHandler),
            ('/chat', ChatHandler),
        ]
        settings = dict(
            debug=True,
            template_path=os.path.join(os.path.dirname(__file__), 'templates')
        )

        super(Application, self).__init__(handlers, **settings)


if __name__ == '__main__':
    app = Application()

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)

    tornado.ioloop.IOLoop.current().start()
