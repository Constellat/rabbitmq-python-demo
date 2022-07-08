#!/usr/bin/env python
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from pika_demo._base import mq_connection


def main():
    connection = mq_connection.get_mq_connection()
    channel = connection.channel()

    # 配置exchange 支持通过routing_key来配置绑定关系
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    routing_key = sys.argv[1] if len(sys.argv) > 1 else 'info'
    message = ' '.join(sys.argv[2:]) or 'Hello World!'
    # 找到对应的exchange，并让其使用routing_key来找到绑定的queue并推送消息
    channel.basic_publish(exchange='direct_logs', routing_key=routing_key, body=message)
    print(" [x] Sent %r" % message)

    # 关闭连接
    connection.close()


if __name__ == '__main__':
    main()
