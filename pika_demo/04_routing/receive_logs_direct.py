#!/usr/bin/env python
# 您需要打开三个控制台。两个将运行 receive_logs_direct.py 脚本。
# 这些控制台将是我们的两个消费者 C1 和 C2。

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from pika_demo._base import mq_connection


def main():
    connection = mq_connection.get_mq_connection()
    channel = connection.channel()

    # exchange_type 为 direct 表示exchange支持按照routing_key 匹配消息到queue
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    print("It's listen the queue_name: " + queue_name)

    severities = sys.argv[1:]
    if not severities:
        sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
        sys.exit(1)

    for severity in severities:
        # 绑定是exchange和queue之间的关系。这可以简单地理解为：queue对来自此exchange的消息感兴趣
        # 绑定可以采用额外的routing_key参数。为了避免与basic_publish参数混淆，我们将其称为 绑定键。
        # 将queue绑定到exchange的每一个routing_key下
        channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)

    def callback(ch, method, properties, body):
        # method.routing_key 可以获得 消息的routing_key
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
