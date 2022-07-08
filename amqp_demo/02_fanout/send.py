#!/usr/bin/env python
import sys, os
import amqp

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from amqp_demo._base import mq_connection


def main():
    conn = mq_connection.get_mq_connection()
    channel = conn.channel()

    channel.exchange_declare(exchange='logs', type='fanout')

    # 第一条消息将只包含一个字符串Hello World！
    message = amqp.Message('Hello World')
    # delivery_mode: Non-persistent(1) or persistent(2)
    message.properties['delivery_mode'] = 2
    channel.basic_publish(msg=message, exchange='logs', routing_key='')
    print(" [x] Sent %s" % message.body)

    channel.close()
    conn.close()


if __name__ == '__main__':
    main()
