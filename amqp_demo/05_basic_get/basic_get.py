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
ROUTING_KEY = 'exchange_demo'


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

    message = amqp.Message('Hello World')
    channel.basic_publish(msg=message, exchange=exchange_name, routing_key=routing_key)
    channel.basic_publish(msg=message, exchange=exchange_name, routing_key=routing_key)
    print(" [x] Sent %s" % message.body)
    print(" [x] Sent %s" % message.body)

    while True:
        try:

            # 消费一条消息，消费逻辑放在 on_message()
            result = channel.basic_get(queue=queue_name, no_ack=False)

            if result:
                print('Received message (routing_key: {}): {}'.format(
                    result.delivery_info.get('routing_key', ''),
                    result.body
                ))
                channel.basic_ack(delivery_tag=result.delivery_info['delivery_tag'])
        except Exception as e:
            print(e)
    channel.close()
    conn.close()


# 最后，在程序关闭期间捕获KeyboardInterrupt。
if __name__ == '__main__':
    main()
