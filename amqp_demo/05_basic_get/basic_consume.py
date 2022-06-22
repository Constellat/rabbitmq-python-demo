#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/6/21 19:57
# @Author: niujianyu
# @File  : queue_demo.py
import sys, os
import amqp

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from amqp_demo._base import mq_connection

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
    channel.queue_declare(queue=queue_name, auto_delete=False, durable=False)
    channel.queue_purge(queue=queue_name)

    channel.exchange_delete(exchange=exchange_name)
    channel.exchange_declare(exchange=exchange_name, type='direct')

    # 将exchange与queue绑定，有新消息，会copy一份发送到该队列
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

    def on_message(message):
        print(" [x] Received %s" % message.body)
        print('Received message (routing_key: {}): {}'.format(
            message.delivery_info.get('routing_key', ''),
            message.body
        ))
        channel.basic_ack(message.delivery_tag)

    message = amqp.Message('Hello World')
    channel.basic_publish(msg=message, exchange=exchange_name, routing_key=routing_key)
    channel.basic_publish(msg=message, exchange=exchange_name, routing_key=routing_key)
    print(" [x] Sent %s" % message.body)
    print(" [x] Sent %s" % message.body)

    channel.basic_consume(queue=queue_name, callback=on_message, no_ack=False)
    while True:
        conn.drain_events()

    channel.close()
    conn.close()


# 最后，在程序关闭期间捕获KeyboardInterrupt。
if __name__ == '__main__':
    main()
