#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/12
@file:07_并行协程.py
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
        ips = [
            '14.130.112.24',
            '15.130.112.24',
            '16.130.112.24',
            '17.130.112.24',
        ]

        rep_1, rep_2 = yield [self.get_ip_info(ips[0]), self.get_ip_info(ips[1])]
        rep_34 = yield dict(rep_3=self.get_ip_info(ips[2]), rep_4=self.get_ip_info(ips[3]))
        self.write_response(ips[0], rep_1)
        self.write_response(ips[1], rep_2)
        self.write_response(ips[2], rep_34['rep_3'])
        self.write_response(ips[3], rep_34['rep_4'])

    def write_response(self, ip, response):
        """输出ip的信息"""
        self.write(ip)
        self.write(':<br/>')
        if response['code'] == 0:
            self.write(response.body)
        else:
            self.write("查询IP信息错误<br/>")

    @tornado.gen.coroutine
    def get_ip_info(self, ip):
        """获取单个IP的信息"""
        http = tornado.httpclient.AsyncHTTPClient()
        response = yield http.fetch(request='http://ip.taobao.com/service/getIpInfo.php?ip={}'.format(ip))

        if response.error:
            rep = {'code': 1}
        else:
            rep = json.loads(response.body.decode('utf-8'))
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
