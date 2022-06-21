#!/usr/bin/env python
from datetime import datetime
import pika, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from pika_demo._base import mq_connection


def main():
    connection = mq_connection.get_mq_connection()
    channel = connection.channel()

    # 配置exchange 支持通过routing_key来配置绑定关系
    arguments = {"x-delayed-type": "direct"}
    channel.exchange_declare(exchange='delayed_exchange', exchange_type='x-delayed-message', arguments=arguments)

    message = 'Hello World!'
    # x-delay 表示消息的延迟消费的时间，这里是5s
    property = pika.BasicProperties(headers={"x-delay": 5 * 1000})
    channel.basic_publish(exchange='delayed_exchange', routing_key="routing_key", body=message, properties=property)
    print(datetime.now())
    print(" [x] Sent %r" % message)

    # 关闭连接
    connection.close()


# 最后，在程序关闭期间捕获KeyboardInterrupt。
if __name__ == '__main__':
    main()
