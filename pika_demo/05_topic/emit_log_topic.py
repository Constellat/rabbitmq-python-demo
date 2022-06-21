#!/usr/bin/env python
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from pika_demo._base import mq_connection


def main():
    connection = mq_connection.get_mq_connection()
    channel = connection.channel()

    # exchange_type 为 topic 表示exchange支持模糊匹配
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    # 在 RabbitMQ 中，消息永远不能直接发送到队列，它总是需要经过一个交换。
    # 队列名称需要在routing_key参数中指定
    # routing_key是多个单词通过.进行分割匹配的
    routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
    message = ' '.join(sys.argv[2:]) or 'Hello World!'
    # 找到对应的exchange，并让其使用routing_key来找到绑定的queue并推送消息
    channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=message)
    print(" [x] Sent %r" % message)

    # 关闭连接
    connection.close()


if __name__ == '__main__':
    main()
