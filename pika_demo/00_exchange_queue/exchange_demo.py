#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/6/21 19:57
# @Author: niujianyu
# @File  : queue_demo.py
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from pika_demo._base import mq_connection

EXCHANGE_NAME = 'exchange_demo'


def main():
    conn = mq_connection.get_mq_connection()  # conn表示连接mq
    channel = conn.channel()  # chan 是开启的一个通道

    exchange_name = EXCHANGE_NAME

    channel.exchange_delete(exchange=exchange_name)
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

    channel.exchange_delete(exchange=exchange_name)

    channel.close()
    conn.close()


# 最后，在程序关闭期间捕获KeyboardInterrupt。
if __name__ == '__main__':
    main()
