#!/usr/bin/env python
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from pika_demo._base import mq_connection


def main():
    # 与 RabbitMQ 服务器建立连接
    connection = mq_connection.get_mq_connection()

    channel = connection.channel()

    # 在发送之前，我们需要确保收件人队列存在。
    # 如果我们向不存在的位置发送消息，RabbitMQ 只会丢弃该消息。
    # 让我们创建一个hello队列，消息将发送到该队列：
    channel.queue_declare(queue='hello')

    # 第一条消息将只包含一个字符串 Hello World！
    # 在 RabbitMQ 中，消息永远不能直接发送到队列，它总是需要经过一个交换。
    # exchange为空则使用默认，routing_key内容就对应队列名称
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body='Hello World!')
    print(" [x] Sent 'Hello World!'")

    # 关闭连接
    connection.close()


if __name__ == '__main__':
    main()
