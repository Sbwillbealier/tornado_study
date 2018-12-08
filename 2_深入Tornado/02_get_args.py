#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/6
@file:05_get_args.py
@desc:
    # 获取查询字符串的参数name的值
        get_query_argument(name, default=_ARG_DEFAULT, strip=True): 如果出现多个同名参数，返回最后一个的值，若为空且未设置default，跑抛出异常
        get_query_arguments(name, strip=True): 返回list,若为空返回[]
        # 获取请求体参数
        get_body_argument(name, default=_ARG_DEFAULT, strip=True): 如果出现多个同名参数，返回最后一个的值
        get_body_arguments(name, strip=True): 如果出现多个同名参数，返回list
        # 获取查询字符串或者请求体中的参数
        get_argument(name, default=_ARG_DEFAULT, strip=True)
        get_arguments(name, strip=True)

    # 请求的其他信息存储在RequestHandler.request中
        method: HTTP请求方式
        host: 被请求主机名
        uri: 请求的完整资源标识，包括路径和查询字符串
        path: 请求的路径部分
        query: 请求的查询字符串部分
        version: 使用的HTTP版本
        headers: 请求的协议头，字典对象，request.headers['Content-Type']获取请求内容类型
        body: 请求体数据，存储文件、图片等二进制数据
        remote_ip: 客户端IP地址
        files: 为用户上传图片，字典类型，self.request.files['image1'][0]['body']获取二进制数据

    # 正则提取uri
        ('/sub-city/(.+)/([a-z]+)', SubjectCityHandler), # 未命名，按从左到右
        ('/sub-date/(?P<subject>.+)/(?P<date>\d+)', SubjectDateHandler), # 命名，按名传递

"""
import tornado.web
from tornado.web import url
import tornado.ioloop
import tornado.httpserver
import tornado.options
import tornado.httpserver

tornado.options.define('port', default=8000, type=int, help='服务器端口')  # 定义服务器监听的端口选项
tornado.options.define('subjects', default=[], type=str, multiple=True,
                       help='multiple value object.')  # 定义多值项


class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""

    def post(self):
        # self.write('hello itcast')
        # self.write('<a href="' + self.reverse_url("python_url") + '">python</a>')
        # 获取查询字符串中的参数
        # query_arg = self.get_query_argument('a')  # 参数名重复，则返回最后一个参数值
        # query_args = self.get_query_arguments('a')  # 参数名重复，返回所有的参数值的list

        # 获取请求体参数
        # body_arg = self.get_body_argument('a')
        # body_args = self.get_body_arguments('a')

        # 从请求体和查询字符串中返回指定参数
        # arg = self.get_argument('c', default='itcast')
        # args = self.get_arguments('a', strip=False)

        # 获取json数据
        # print(self.request.headers['Content-Type'])
        # if self.request.headers['Content-Type']==('application/json'):
        #     json_data = self.request.body
        #     json_data = json.loads(json_data.decode('utf-8'))
        #     self.write(str(json_data))

        # 获取文件
        print(type(self.request.files))
        # print(self.request.files['image1'][0])
        filename = self.request.files['image1'][0]['filename']
        # print(self.request.files['image1'][0]['body'])
        print(self.request.files['image1'][0]['content_type'])
        with open(filename, 'wb') as f:
            f.write(self.request.files['image1'][0]['body'])


class ItcastHandler(tornado.web.RequestHandler):
    """传字典的路由处理类"""

    def initialize(self, subjects):
        # 对于路由中的字典， 会传入对应的RequestHandler的initialize()方法中
        self.subjects = subjects

    def get(self, *args, **kwargs):
        self.write(self.subjects)


class SubjectCityHandler(tornado.web.RequestHandler):
    def get(self, subject, city):
        self.write("Subject: %s <br> City: %s" % (subject, city))


class SubjectDateHandler(tornado.web.RequestHandler):
    def get(self, date, subject):
        self.write("Date: %s <br>Subject: %s" % (date, subject))


if __name__ == '__main__':
    print(tornado.options.options.subjects)

    app = tornado.web.Application([
        ('/', IndexHandler),
        ('/cpp', ItcastHandler, {'subjects': 'C++'}),
        url('/python', ItcastHandler, {'subjects': 'python'}, name='python_url'),
        ('/sub-city/(.+)/([a-z]+)', SubjectCityHandler),
        ('/sub-date/(?P<subject>.+)/(?P<date>\d+)', SubjectDateHandler),
    ], debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()
