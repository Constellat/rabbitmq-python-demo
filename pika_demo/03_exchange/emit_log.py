#!/usr/bin/env python
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from pika_demo._base import mq_connection


def main():
    connection = mq_connection.get_mq_connection()
    channel = connection.channel()

    # 在建立连接后，我们声明了exchange。此步骤是必要的，因为禁止发布到不存在的exchange。
    # fanout的exchange将收到的所有消息广播到它知道的所有队列。这正是我们的记录器所需要的。
    # 如果没有队列绑定到exchanges，消息将丢失，但这对我们来说没关系；如果没有消费者在监听，我们可以安全地丢弃消息。
    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    # 在 RabbitMQ 中，消息永远不能直接发送到队列，它总是需要经过一个交换。
    # 队列名称需要在routing_key参数中指定
    message = ' '.join(sys.argv[1:]) or "Hello World!"
    # 之前没有exchange的值，消息被路由到具有routing_key指定的名称的队列（如果存在）。
    channel.basic_publish(exchange='logs', routing_key='', body=message)
    print(" [x] Sent %r" % message)

    # 关闭连接
    connection.close()


if __name__ == '__main__':
    main()
