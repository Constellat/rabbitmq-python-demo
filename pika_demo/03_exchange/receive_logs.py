#!/usr/bin/env python
# 您需要打开三个控制台。两个将运行 receive_logs.py 脚本。
# 这些控制台将是我们的两个消费者 C1 和 C2。

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from pika_demo._base import mq_connection


def main():
    connection = mq_connection.get_mq_connection()
    channel = connection.channel()

    # fanout的exchange将收到的所有消息广播到它知道的所有队列。这正是我们的记录器所需要的。
    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    # queue=''  让服务器为我们选择一个随机队列名称
    # 此时result.method.queue包含一个随机队列名称。
    # 一旦消费者连接关闭，队列应该被删除。
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    print("It's listen the queue_name: " + queue_name)
    # 将exchange与queue绑定，有新消息，会copy一份发送到该队列
    channel.queue_bind(exchange='logs', queue=queue_name)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    # 我们进入一个永无止境的循环，等待数据并在必要时运行回调
    channel.start_consuming()


# 最后，在程序关闭期间捕获KeyboardInterrupt。
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
