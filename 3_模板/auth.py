#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/7
@file:test.py
@desc:
    用户认证：
        authenticated装饰器：
            给需要认证用户的处理函数加上装饰器，只有存在合法用户才允许调用
            判断依据来源于请求处理类中的self.current_user属性，而这个属性值是self.get_current_user()的返回值

        get_current_user()：
            验证用户的逻辑，并返回user_name，返回非空即可验证用户

    数据库错误unread result found

"""
import os
import json
import time
from tornado.web import RequestHandler
from tornado.httpserver import HTTPServer
import tornado.ioloop
import mysql.connector


# 自定义函数（过滤器）
def house_title_join(titles):
    return '-'.join(titles)


class IndexHandler(RequestHandler):
    """首页handler类"""

    def get(self):
        # self.write('index')

        # 查询数据库
        query = 'select hi_title,hi_address,hi_price from ih_house_info'
        # 拿到游标
        cursor = self.application.db.cursor()
        # 执行查询
        cursor.execute(query)
        # 读取结果
        result = cursor.fetchone()
        print(result)

        # 构造数据
        houses = [
            {
                "price1": result[2],
                "price2": 200,
                "title": ["宽窄巷子", "160平大空间", "文化保护区双地铁"],
                "score": 5,
                "comments": 6,
                "position": result[1],
            }
        ]
        # # 关闭游标
        # cursor.close()

        # 设置cookie
        self.set_cookie('n1', 'v1')
        self.set_cookie('n2', 'v2')
        self.set_cookie('n3', 'v3', expires=time.strptime('2018-12-9 20:36:59', "%Y-%m-%d %H:%M:%S"))
        self.set_cookie('n4', 'v4', expires=time.mktime(time.strptime('2018-12-9 20:36:59', "%Y-%m-%d %H:%M:%S")))

        # 获取cookie
        print(self.get_cookie('n1'))
        print(self.get_cookie('n2'))
        print(self.get_cookie('n3'))
        print(self.get_cookie('n4'))

        # 使用render渲染并返回模板
        self.render('index.html', houses=houses, house_title_join=house_title_join)


class ProfileHandler(RequestHandler):
    """用户信息处理类"""

    def get_current_user(self):
        """在此完成用户验证的操作，只有返回非空即可验证"""
        user_name = self.get_cookie('name', None)
        return user_name

    @tornado.web.authenticated
    def get(self):
        self.write('这是我的个人主页')


class LoginHandler(RequestHandler):
    """登录处理类"""

    def get(self):
        next = self.get_argument('next', '/')
        self.render('login.html', next=next)

    def post(self):
        """登录完成跳转到原页面"""
        user_name = self.get_argument('user_name')
        next = self.get_argument('next')
        self.set_cookie('name', user_name)
        self.redirect(next)


class Application(tornado.web.Application):
    """自定义应用类"""

    def __init__(self):
        current_path = os.path.dirname(__file__)

        handlers = [
            ('/', IndexHandler),
            ('/profile', ProfileHandler),
            ('/login', LoginHandler),
        ]

        settings = {
            'template_path': os.path.join(current_path, 'templates'),
            'static_path': os.path.join(current_path, 'statics'),
            'debug': True,
            'cookie_secret': 'brlXmGnISDK7FXKnJ9O4f+XbWSak6EkDkKLeQzWEjR0=',
            'xsrf_cookies': True,
            'login_url': '/login',
        }

        super(Application, self).__init__(handlers, **settings)

        # 每个handler可以通过 self.application.db 获取连接数据库对象
        self.db = mysql.connector.connect(
            user='root',
            password='root',
            host='127.0.0.1',
            database='ihome',
            buffered=True,
        )
        self.db.autocommit = True  # 设置为自动提交


if __name__ == '__main__':
    current_path = os.path.dirname(__file__)

    app = Application()

    http_server = HTTPServer(app)
    http_server.listen(8000)

    tornado.ioloop.IOLoop.current().start()
