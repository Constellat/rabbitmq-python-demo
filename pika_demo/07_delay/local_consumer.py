#!/usr/bin/env python
from datetime import datetime
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from pika_demo._base import mq_connection


def main():
    connection = mq_connection.get_mq_connection()
    channel = connection.channel()

    # 这个参数决定你用的exchange的绑定和匹配方式是什么
    arguments = {"x-delayed-type": "direct"}
    channel.exchange_declare(exchange='delayed_exchange', exchange_type='x-delayed-message', arguments=arguments)

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    print("It's listen the queue_name: " + queue_name)

    channel.queue_bind(exchange='delayed_exchange', queue=queue_name, routing_key="routing_key")

    def callback(ch, method, properties, body):
        print(" [x] Received %r:%r" % (method.routing_key, body))
        # properties.headers.get('x-delay') 可以获取消息头部的延迟时间
        print(properties.headers.get('x-delay'))
        print(datetime.now())
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
