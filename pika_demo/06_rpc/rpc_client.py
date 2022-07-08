#!/usr/bin/env python
import pika, sys, os
import uuid

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from pika_demo._base import mq_connection


class FibonacciRpcClient(object):

    def __init__(self):
        self.connection = mq_connection.get_mq_connection()
        self.channel = self.connection.channel()

        # 申请一个queue 作为rpc执行结果传回时使用
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        # 轮询等待执行结果
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


def main():
    fibonacci_rpc = FibonacciRpcClient()

    print(" [x] Requesting fib(30)")
    response = fibonacci_rpc.call(30)
    print(" [.] Got %r" % response)


if __name__ == '__main__':
    main()
