#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/10
@file:01_回调实现异步.py
@desc:
"""
import time
import _thread


def long_time_io(cb):
    def fun(callback):
        print('开始执行耗时操作')
        time.sleep(5)

        # 执行完毕回调函数返回结果
        callback('io result')

    # 耗时操作单开一个线程执行
    _thread.start_new_thread(fun, (cb,))
    # threading.Thread(fun, (cb,))


def on_finish(ret):
    print('开始执行回调函数')
    print('耗时操作结果ret:{}'.format(ret))


def req_a():
    print('开始处理a')
    long_time_io(on_finish)
    print('离开处理a')


def req_b():
    print('开始处理b')
    time.sleep(2)
    print('离开处理b')


def main():
    req_a()
    req_b()

    # 主程序不关闭
    while 1:
        pass


if __name__ == '__main__':
    main()
