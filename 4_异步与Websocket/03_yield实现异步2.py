#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/10
@file:yield异步.py
@desc:
    解决要将req_a视为生成器的麻烦
"""
import time
import _thread

# 全局生成器对象
gen = None


# 装饰器完成生产器生成和调用next()
def gen_coroutine(fun):
    def wrapper():
        global gen
        gen = fun()
        gen.__next__()

    return wrapper


def long_time_io():
    def fun():
        print('开始执行耗时操作')
        time.sleep(5)

        try:
            global gen
            gen.send('耗时操作执行完成')  # 使用send返回结果并唤醒主程序继续执行
        except StopIteration:
            # 捕获生成器完成迭代，防止程序退出
            pass

    # 耗时操作单开一个线程执行
    _thread.start_new_thread(fun, ())


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
