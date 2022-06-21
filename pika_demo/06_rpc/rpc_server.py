#!/usr/bin/env python
import pika
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__),"../.."))
from pika_demo._base import mq_connection


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def main():
    connection = mq_connection.get_mq_connection()
    channel = connection.channel()

    channel.queue_declare(queue='rpc_queue')

    def on_request(ch, method, props, body):
        n = int(body)
        print(" [.] fib(%s)" % n)
        # 业务方法或者计算任务执行
        response = fib(n)
        # 回传执行结果的queue 存放在props.reply_to
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

    print(" [x] Awaiting RPC requests")
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
