#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/12
@file:06_tornado协程异步.py
@desc:
"""
import json
import tornado.web
import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.httpclient


class IndexHandler(tornado.web.RequestHandler):
    """首页handler类"""

    @tornado.gen.coroutine  # 不关闭连接，也不发送响应
    def get(self):
        """异步请求客户端"""
        ip = self.get_argument('ip')

        # 方式一
        # http = tornado.httpclient.AsyncHTTPClient()
        # response = yield http.fetch(request='http://ip.taobao.com/service/getIpInfo.php?ip={}'.format(ip))
        #
        # if response.error:
        #     self.send_error(500)
        # else:
        #     data = json.loads(response.body.decode('utf-8'))
        #     if data['code'] == 0:
        #         self.write(data)
        #     else:
        #         self.write('查询ip地址失败！')
        #     self.finish()

        # 方式二
        response = yield self.get_ip_info(ip)
        if response['code'] == 0:
            self.write(response)
        else:
            self.write('查询ip地址失败！')
        self.finish()

    @tornado.gen.coroutine
    def get_ip_info(self, ip):
        """将异步web请求单独出来"""
        http = tornado.httpclient.AsyncHTTPClient()
        response = yield http.fetch(request='http://ip.taobao.com/service/getIpInfo.php?ip={}'.format(ip))
        if response.error:
            rep = {"code:": 1}
        else:
            rep = json.loads(response.body.decode('utf-8'))
        # yield后不能跟return，使用tornado定义的异常抛出去
        raise tornado.gen.Return(rep)


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
