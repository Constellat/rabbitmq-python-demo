#!/usr/bin/env python
from datetime import datetime
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from amqp_demo._base import mq_connection


def main():
    conn = mq_connection.get_mq_connection()  # conn表示连接mq
    channel = conn.channel()  # chan 是开启的一个通道

    # 这个参数决定你用的exchange的绑定和匹配方式是什么
    arguments = {"x-delayed-type": "direct"}
    channel.exchange_declare(exchange='delayed_exchange', type='x-delayed-message',
                             arguments=arguments,
                             auto_delete=False)

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.queue
    print("It's listen the queue_name: " + queue_name)

    channel.queue_bind(exchange='delayed_exchange', queue=queue_name, routing_key="routing_key")

    def on_message(message):
        print(" [x] Received %s" % message.body)
        # properties.headers.get('x-delay') 可以获取消息头部的延迟时间
        # print(properties.headers.get('x-delay'))
        print(message.properties.get('application_headers',{}).get('x-delay', 0))
        print('Received message (routing_key: {}): {}'.format(
            message.delivery_info.get('exchange', ''),
            message.body
        ))
        print(datetime.now())
        print(" [x] Done")
        channel.basic_ack(message.delivery_tag)

    channel.basic_consume(queue=queue_name, callback=on_message)
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
