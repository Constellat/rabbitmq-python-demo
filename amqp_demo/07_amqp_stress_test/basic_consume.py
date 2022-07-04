#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/6/21 19:57
# @Author: niujianyu
# @File  : queue_demo.py
import sys, os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from amqp_demo._base import mq_connection

QUEUE_NAME = 'queue_demo'
start_time = 0

def main():
    conn = mq_connection.get_mq_connection()  # conn表示连接mq
    channel = conn.channel()  # chan 是开启的一个通道

    queue_name = 'test_fanout'

    def on_message(message):
        global start_time
        print(" [x] Received %s" % message.body)
        number = int(message.body.split(' ')[2])
        print('Received message (routing_key: {}): {}'.format(
            message.delivery_info.get('routing_key', ''),
            message.body
        ))
        ret = 0.01 * (number % 10 + 1)
        time.sleep(ret)
        print(ret)
        if number == 0:
            start_time = time.time()
        elif number == 29999:
            end_time = time.time()
            print("start_time: %s" % start_time)
            print("end_time: %s" % end_time)
            print("waste_time: %s" % (end_time - start_time))
        channel.basic_ack(delivery_tag=message.delivery_tag)

    channel.basic_consume(queue=queue_name, callback=on_message, no_ack=False)
    while True:
        conn.drain_events()

    channel.close()
    conn.close()


# 最后，在程序关闭期间捕获KeyboardInterrupt。
if __name__ == '__main__':
    main()
