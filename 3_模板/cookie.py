#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/7
@file:test.py
@desc:
    cookie:
        # 设置cookie
        set_cookie(name, value, domain=None, expires=None, path='/', expires_days=None)
            默认会话结束是过期

        # 获取cookie
        get_cookie(name, default=None)

        # 清除(将cookie值设为空，并使其过期)
        clear_cookie(name, path='/', domain=None)
        clear_all_cookies(path='/'， domain=None)

        # 设置、获取安全cookie
        cookie_secret = 'brlXmGnISDK7FXKnJ9O4f+XbWSak6EkDkKLeQzWEjR0='

        set_secure_cookie(name, value, expires_days=30)
        get_secure_cookie(name, value=None, max_age_days=31)

        # csrf攻击防护
        xsrf_cookies = True

        # 模板中应用xsrf保护
        form表单中添加隐藏字段 {% module xsrf_form_html() %}

        # 非模板应用
            # 设置_xsrf的Cookie值, 在任意的handler中通过获取self.xsrf_token的值来生成_xsrf并设置cookie
                # 一种动态请求，写专用的接口来设置_xsrf
                # 一种获取静态文件请求，重写StaticFileHandler初始化时设置_xsrf

        # 请求需携带_xsrf参数
            # 请求体为form表单，可以在请求体中添加_xsrf参数
            # 请求体为json或者xml格式，可以设置HTTP头X-XSRFToken来传递_xsrf值

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


class XSRFTestHandler(RequestHandler):
    """测试请求体携带_xsrf参数"""

    def get(self):
        # self.render('xsrf.html')
        self.render('json.html')

    def post(self):
        # 从请求体中接收数据
        # v1 = self.get_argument('k1')
        # _xsrf = self.get_argument('_xsrf')
        # print(v1)
        # print(_xsrf)

        # 从json中读取数据
        if self.request.headers['Content-Type'] == ('application/json'):
            json_data = self.request.body
            json_data = json.loads(json_data.decode('utf-8'))
            print(json_data)


class XSRFTokenHandler(RequestHandler):
    """专门用来设置_xsrf Cookie的接口"""

    def get(self):
        self.xsrf_token
        self.write('ok')


class StaticFileHandler(tornado.web.StaticFileHandler):
    """重写StaticFileHandler，构造时触发设置_xsrf Cookie"""

    def __init__(self):
        super(StaticFileHandler, self).__init__()
        self.xsrf_token


class ClearOneCookieHandler(RequestHandler):
    """"清除一个cookie的handler"""

    def get(self):
        # 清除cookie
        self.clear_cookie('n1')
        self.write('OK')


class ClearAllCookieHandler(RequestHandler):
    """清除所有cookie的handler"""

    def get(self):
        # 清除cookie
        self.clear_all_cookies()
        self.write('OK')


class SecureCookieHandler(RequestHandler):
    """安全cookie"""

    def get(self):
        """页面访问次数+1"""
        cookie = self.get_secure_cookie('count')
        count = int(cookie) + 1 if cookie else 1
        self.set_secure_cookie('count', str(count), path='/count', expires_days=1)
        self.write("<h1>您已经访问本页面%d次</h1>" % count)


class NewHandler(RequestHandler):

    def get(self):
        self.render('new.html', text="")

    def post(self):
        text = self.get_argument('text', "")

        # chrome设置请求头，可关闭浏览器XSS拦截
        self.set_header('X-XSS-Protection', 0)
        self.render('new.html', text=text)


class InsertUserHandler(RequestHandler):
    """添加用户handler"""

    def get(self):
        self.render('add_user.html')

    def post(self):
        name = self.get_argument('name')
        passwd = self.get_argument('passwd')
        mobile = self.get_argument('mobile')

        sql = "insert into ih_user_info(ui_name, ui_mobile, ui_passwd) value(%s, %s, %s)"
        cursor = self.application.db.cursor()
        cursor.execute(sql, (name, mobile, passwd))
        print(cursor.rowcount)
        self.write('受影响： %s' % cursor.rowcount)


class GetHouseHandler(RequestHandler):
    """查询某用户旗下的房产"""

    def get(self):
        """访问方式为http://127.0.0.1/get?id=111"""
        uid = self.get_argument('id')
        cursor = self.application.db.cursor()
        sql = "select ui_name, hi_title, hi_address, hi_price from ih_house_info inner join ih_user_info on hi_user_id = ui_user_id where ui_user_id=%s"
        try:
            cursor.execute(sql, (uid,))
        except Exception as e:
            return self.write({"code": 1, "status": 'db error', 'data': ''})
        houses = []
        results = cursor.fetchall()
        if results:
            for result in results:
                house = {
                    'uname': result[0],
                    'htitle': result[1],
                    'haddress': result[2],
                    'hprice': result[3],
                }
                houses.append(house)
            self.write({"code": 0, "status": "OK", "data": houses})


class Application(tornado.web.Application):
    """自定义应用类"""

    def __init__(self):
        current_path = os.path.dirname(__file__)

        handlers = [
            ('/', IndexHandler),
            ('/insert', InsertUserHandler),
            ('/get_house', GetHouseHandler),
            ('/clear_one', ClearOneCookieHandler),
            ('/clear_all', ClearAllCookieHandler),
            ('/count', SecureCookieHandler),
            ('/test_xsrf', XSRFTestHandler),
        ]

        settings = {
            'template_path': os.path.join(current_path, 'templates'),
            'static_path': os.path.join(current_path, 'statics'),
            'debug': True,
            'cookie_secret': 'brlXmGnISDK7FXKnJ9O4f+XbWSak6EkDkKLeQzWEjR0=',
            'xsrf_cookies': True,
        }

        super(Application, self).__init__(handlers, **settings)

        # 每个handler可以通过 self.application.db 获取连接数据库对象
        self.db = mysql.connector.connect(
            user='root',
            password='root',
            host='127.0.0.1',
            database='ihome'
        )
        self.db.autocommit = True  # 设置为自动提交


if __name__ == '__main__':
    current_path = os.path.dirname(__file__)

    app = Application()

    http_server = HTTPServer(app)
    http_server.listen(8000)

    tornado.ioloop.IOLoop.current().start()
