#!/usr/bin/env python
# 您需要打开三个控制台。两个将运行 receive_logs_topic.py 脚本。
# 这些控制台将是我们的两个消费者 C1 和 C2。

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from amqp_demo._base import mq_connection


def main():
    conn = mq_connection.get_mq_connection()  # conn表示连接mq
    channel = conn.channel()  # chan 是开启的一个通道

    # exchange_type 为 topic 表示exchange支持模糊匹配
    channel.exchange_declare(exchange='topic_logs', type='topic', auto_delete=False)

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.queue
    print("It's listen the queue_name: " + queue_name)

    binding_keys = sys.argv[1:]
    if not binding_keys:
        sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
        sys.exit(1)

    for binding_key in binding_keys:
        # 这里的绑定的routing_key 支持通配符
        channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)

    def on_message(message):
        print(" [x] Received %s: %s" % (message.delivery_info.get('routing_key'), message.body))
        print('Received message (routing_key: {}): {}'.format(
            message.delivery_info.get('routing_key', ''),
            message.body
        ))
        print(" [x] Done")

        channel.basic_ack(message.delivery_tag)

    channel.basic_consume(queue=queue_name, callback=on_message)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    while True:
        conn.drain_events()


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
