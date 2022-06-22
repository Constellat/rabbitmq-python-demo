#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/6/21 19:57
# @Author: niujianyu
# @File  : queue_demo.py
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from pika_demo._base import mq_connection

QUEUE_NAME = 'queue_demo'
EXCHANGE_NAME = 'exchange_demo'
ROUTING_KEY = 'queue_demo'


def main():
    conn = mq_connection.get_mq_connection()  # conn表示连接mq
    channel = conn.channel()  # chan 是开启的一个通道

    queue_name = QUEUE_NAME
    exchange_name = EXCHANGE_NAME
    routing_key = ROUTING_KEY

    channel.queue_delete(queue=queue_name)
    # 声明(新建)队列
    channel.queue_declare(queue=queue_name, auto_delete=False, durable=False)
    # 清空队列
    channel.queue_purge(queue=queue_name)

    channel.exchange_delete(exchange=exchange_name)
    # 声明(新建) Exchange
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

    # 将exchange与queue绑定，有新消息，会copy一份发送到该队列
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

    # 队列解绑 参数和绑定完全一致
    channel.queue_unbind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

    # 删除队列
    channel.queue_delete(queue=queue_name)

    # 删除Exchange
    channel.exchange_delete(exchange=exchange_name)

    channel.close()
    conn.close()


# 最后，在程序关闭期间捕获KeyboardInterrupt。
if __name__ == '__main__':
    main()
