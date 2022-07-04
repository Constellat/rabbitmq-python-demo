#!/usr/bin/env python
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from amqp_demo._base import mq_connection


def main():
    conn = mq_connection.get_mq_connection()  # conn表示连接mq
    channel = conn.channel()  # chan 是开启的一个通道

    channel.exchange_declare(exchange='logs', type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.queue
    print("It's listen the queue_name: " + queue_name)

    # 将exchange与queue绑定，有新消息，会copy一份发送到该队列
    channel.queue_bind(exchange='logs', queue=queue_name)

    def on_message(message):
        print(" [x] Received %s" % message.body)
        print('Received message (delivery tag: {}): {}'.format(message.delivery_tag, message.body))
        channel.basic_ack(message.delivery_tag)

    # 消费一条消息，消费逻辑放在 on_message()
    channel.basic_consume(queue=queue_name, callback=on_message)
    # result = chan.basic_get(queue='test_fanout', no_ack=False)
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
