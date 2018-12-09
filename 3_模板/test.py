#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/7
@file:test.py
@desc:
    static_path: 用来告诉tornado从文件系统中的一个特定位置提供静态资源，必须在 host:port/static/ 后面
        http://127.0.0.1:8000/static/images/杭州轨道交通图2022.png



    StaticFileHandler: 直接用来处理静态文件的处理函数
        path: 指定静态文件的根目录，并在 此目录下寻找路由中用正则表达式提取的文件名
        default_filename: 访问此路径未提供文件名时，默认使用的文件
        http://127.0.0.1:8000/images/杭州轨道交通图2022.png

"""
import os
from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado.httpserver import HTTPServer
import tornado.ioloop


# 自定义函数（过滤器）
def house_title_join(titles):
    return '-'.join(titles)


class IndexHandler(RequestHandler):

    def get(self):
        # self.write('index')

        # 构造数据
        houses = [
            {
                "price1": 300,
                "price2": 302,
                "title": ["宽窄巷子", "160平大空间", "文化保护区双地铁"],
                "score": 5,
                "comments": 6,
                "position": "小和山",
            },
            {
                "price1": 300,
                "price2": 302,
                "title": ["宽窄巷子", "160平大空间", "文化保护区双地铁"],
                "score": 5,
                "comments": 6,
                "position": "小和山",
            },
            {
                "price1": 300,
                "price2": 302,
                "title": ["宽窄巷子", "160平大空间", "文化保护区双地铁"],
                "score": 5,
                "comments": 6,
                "position": "小和山",
            },
        ]

        # 使用render渲染并返回模板
        self.render('index.html', houses=houses, house_title_join=house_title_join)


class NewHandler(RequestHandler):

    def get(self):
        self.render('new.html', text="")

    def post(self):
        text = self.get_argument('text', "")

        # chrome设置请求头，可关闭浏览器XSS拦截
        self.set_header('X-XSS-Protection', 0)
        self.render('new.html', text=text)


if __name__ == '__main__':
    current_path = os.path.dirname(__file__)

    app = Application([
        ('/', IndexHandler),
        ('/new', NewHandler),
        ('/static/(.*)', StaticFileHandler,
         {'path': os.path.join(current_path, 'statics/html'), 'default_filename': 'index.html'}),
    ],
        debug=True,
        static_path=os.path.join(current_path, 'statics'),
        template_path=os.path.join(current_path, 'templates'),
        autoescape=None,
    )

    http_server = HTTPServer(app)
    http_server.listen(8000)

    tornado.ioloop.IOLoop.current().start()
