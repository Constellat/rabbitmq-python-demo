#!/usr/bin/env python
import amqp, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from amqp_demo._base import mq_connection


def main():
    connection = mq_connection.get_mq_connection()
    channel = connection.channel()

    # durable 将其声明为耐用的：即使 RabbitMQ 重新启动，队列也不会丢失
    # 针对已经创建的queue，无法修改其持久性，新加一个queue叫task_queue
    channel.queue_declare(queue='task_queue', durable=True, auto_delete=False)

    message = amqp.Message('Hello World')
    # delivery_mode: Non-persistent(1) or persistent(2)
    message.properties['delivery_mode'] = 2
    channel.basic_publish(msg=message, exchange='', routing_key='task_queue')
    print(" [x] Sent %r" % message)

    # 关闭连接
    connection.close()


if __name__ == '__main__':
    main()
