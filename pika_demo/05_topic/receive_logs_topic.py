#!/usr/bin/env python
# 您需要打开三个控制台。两个将运行 receive_logs_topic.py 脚本。
# 这些控制台将是我们的两个消费者 C1 和 C2。

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from pika_demo._base import mq_connection


def main():
    connection = mq_connection.get_mq_connection()
    channel = connection.channel()

    # exchange_type 为 topic 表示exchange支持模糊匹配
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    print("It's listen the queue_name: " + queue_name)

    binding_keys = sys.argv[1:]
    if not binding_keys:
        sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
        sys.exit(1)

    for binding_key in binding_keys:
        # 这里的绑定的routing_key 支持通配符
        channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)

    def callback(ch, method, properties, body):
        print(" [x] Received %r:%r" % (method.routing_key, body))
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
