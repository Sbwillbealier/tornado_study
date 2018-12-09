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
from tornado.web import RequestHandler, StaticFileHandler
from tornado.httpserver import HTTPServer
import tornado.ioloop
import mysql.connector


# 自定义函数（过滤器）
def house_title_join(titles):
    return '-'.join(titles)


class IndexHandler(RequestHandler):

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


class InsertHandler(RequestHandler):
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
            ('/insert', InsertHandler),
            ('/get_house', GetHouseHandler),
        ]

        settings = {
            'template_path': os.path.join(current_path, 'templates'),
            'static_path': os.path.join(current_path, 'statics'),
            'debug': True,
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
