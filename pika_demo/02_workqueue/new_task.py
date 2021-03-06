#!/usr/bin/env python
import pika, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from pika_demo._base import mq_connection


def main():
    connection = mq_connection.get_mq_connection()
    channel = connection.channel()

    # durable 将其声明为耐用的：即使 RabbitMQ 重新启动，队列也不会丢失
    # 针对已经创建的queue，无法修改其持久性，新加一个queue叫task_queue
    channel.queue_declare(queue='task_queue', durable=True)

    # delivery_mode=PERSISTENT_DELIVERY_MODE：将我们的消息标记为持久的
    # 即使 RabbitMQ 重新启动，消息也不会丢失，必须依赖队列queue是durable的
    # 将消息标记为持久性并不能完全保证消息不会丢失。
    # 虽然它告诉 RabbitMQ 将消息保存到磁盘，但是当 RabbitMQ 接受消息并且还没有保存它时，仍然有很短的时间窗口。
    # 它可能只是保存到缓存中而不是真正写入磁盘, 持久性保证并不强。如果您需要更强的保证，那么您可以使用 发布者确认。
    message = ' '.join(sys.argv[1:]) or "Hello World!"
    channel.basic_publish(exchange='', routing_key='task_queue', body=message,
                          properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
    print(" [x] Sent %r" % message)

    # 关闭连接
    connection.close()


if __name__ == '__main__':
    main()
