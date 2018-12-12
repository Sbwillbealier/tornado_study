#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/10
@file:yield异步.py
@desc:
    解决存在全局变量gen的麻烦
"""
import time
import _thread


# # 全局生成器对象
# gen = None


# 装饰器完成生产器生成和调用next()
def gen_coroutine(f):
    def wrapper():
        gen_a = f()  # 生成器req_a
        gen_l = gen_a.__next__()  # 生成器long_time_io

        def fun():
            result = gen_l.__next__()  # 执行long_time_io
            try:
                gen_a.send(result)  # 将耗时结果反馈给主线程并使其继续执行下去
            except StopIteration:
                pass

        _thread.start_new_thread(fun, ())

    return wrapper


def long_time_io():
    print('开始执行耗时操作')
    time.sleep(5)
    print('耗时操作执行完成')
    yield 'io result'


@gen_coroutine
def req_a():
    print('开始处理a')
    result = yield long_time_io()
    print('耗时操作结果result:{}'.format(result))
    print('离开处理a')


def req_b():
    print('开始处理b')
    time.sleep(2)
    print('离开处理b')


def main():
    # req_a()是生成器函数，下面代码类似同步代码一样，顺序执行
    # global gen
    # gen = req_a()
    # gen.__next__()  # long_time_io
    req_a()
    req_b()

    # 主程序不关闭
    while 1:
        pass


if __name__ == '__main__':
    main()
