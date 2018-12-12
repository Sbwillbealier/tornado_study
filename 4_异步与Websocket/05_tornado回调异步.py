#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/12
@file:05_tornado回调异步.py
@desc:
    1. tornado.httpclient.AsyncHTTPClient
        用于异步请求的web请求客户端

        fetch(request, callback=None)
            执行一个web请求，并异步返回一个HTTPResponse响应

"""
import json
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.httpclient


class IndexHandler(tornado.web.RequestHandler):
    """首页handler类"""

    @tornado.web.asynchronous  # 不关闭连接，也不发送响应
    def get(self):
        """异步请求客户端"""
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch(request='http://ip.taobao.com/service/getIpInfo.php?ip=167.23.35.36', callback=self.on_response)

        # get之后就是finish，不在添加到缓冲区

    def on_response(self, response):
        """异步请求的响应处理"""
        if response.error:
            self.send_error(500)
        else:
            data = json.loads(response.body.decode('utf-8'))
            self.write(data)
        self.finish()


class Application(tornado.web.Application):
    """应用对象类"""

    def __init__(self):
        handlers = [
            ('/', IndexHandler),
        ]
        settings = dict(
            debug=True,
        )

        super(Application, self).__init__(handlers, **settings)


if __name__ == '__main__':
    app = Application()

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)

    tornado.ioloop.IOLoop.current().start()
