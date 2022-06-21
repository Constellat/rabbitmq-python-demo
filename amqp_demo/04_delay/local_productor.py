#!/usr/bin/env python
from datetime import datetime
import sys, os
import amqp

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from amqp_demo._base import mq_connection


def main():
    conn = mq_connection.get_mq_connection()
    channel = conn.channel()

    # 配置exchange 支持通过routing_key来配置绑定关系
    arguments = {"x-delayed-type": "direct"}
    channel.exchange_declare(exchange='delayed_exchange', type='x-delayed-message',
                             arguments=arguments,
                             auto_delete=False)

    # 第一条消息将只包含一个字符串Hello World！
    header = {"x-delay": 5 * 1000}
    message = amqp.Message(body='Hello World', application_headers=header)
    channel.basic_publish(exchange='delayed_exchange', routing_key="routing_key", msg=message)
    print(datetime.now())
    print(" [x] Sent %s" % message.body)

    channel.close()
    conn.close()


if __name__ == '__main__':
    main()
