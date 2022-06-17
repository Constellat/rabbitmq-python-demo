#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/6/10 15:03
# @Author: niujianyu
# @File  : local_server.py
import amqp
from six.moves import cPickle
import importlib

RABBIT_HOST = "localhost"
RABBIT_TCP_PORT = 5672
RABBIT_USER = "admin"
RABBIT_PASSWORD = "admin"
VIRTUAL_HOST = "/"
EXCHANGE_NAME = "rmi_test_topic"
QUEUE_NAME = "rmi_test_topic"
ROUTING_KEY = "rmi.test.topic"
conn = None


def get_rabbit_chan():
    global conn
    if not conn or not conn.connected:
        conn = amqp.Connection(host="%s:%s" % (RABBIT_HOST, RABBIT_TCP_PORT), userid=RABBIT_USER,
                               password=RABBIT_PASSWORD,
                               virtual_host=VIRTUAL_HOST)
    chan = conn.channel()
    return chan


def create_queue(name, auto_delete=False, durable=True, arguments=None):
    queue_name = name
    chan = get_rabbit_chan()
    chan.queue_delete(queue=queue_name)
    chan.queue_declare(
        queue=queue_name, auto_delete=auto_delete, durable=durable, arguments=arguments)
    # 清空队列
    chan.queue_purge(queue=queue_name)
    return queue_name


def create_exchange(name, change_type='fanout', auto_delete=False, durable=True, arguments=None):
    exchange_name = name
    chan = get_rabbit_chan()
    chan.exchange_delete(exchange=exchange_name)
    chan.exchange_declare(
        exchange=exchange_name, auto_delete=auto_delete, type=change_type, durable=durable, arguments=arguments)
    return exchange_name


def create_binding(queue_name, exchange_name, routing_key=''):
    chan = get_rabbit_chan()
    chan.queue_bind(queue=queue_name, exchange=exchange_name, routing_key=routing_key)


def invoke_method(my_message):
    class_name = my_message.class_name
    func_name = my_message.func_name
    module_path = my_message.module_path
    kwargs = my_message.kwargs

    print('类名字：%s，函数名字:%s, 包路径:%s, 函数参数:%s' % (class_name, func_name, module_path, kwargs))
    module = importlib.import_module(module_path)
    if class_name:
        cls = getattr(module, class_name)
        print(type(cls))
        func = getattr(cls, func_name)
        print(type(func))
        func(**kwargs)


def consume_msg(queue_name):
    chan = get_rabbit_chan()

    def on_message(message):
        body = cPickle.loads(message.body)
        print(" [x] Received %s: %s" % (message.delivery_info.get('routing_key'), message.body))
        print('Received message (delivery tag: {}): {}'.format(message.delivery_tag, message.body))
        try:
            invoke_method(body)
        except Exception as e:
            print("Consume Error!!!!")
            print("Exception: %s", e)
        print(" [x] Done")

        chan.basic_ack(message.delivery_tag)

    # 消费一条消息，消费逻辑放在 on_message()
    chan.basic_consume(queue=queue_name, callback=on_message)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    while True:
        conn.drain_events()


def invoke_background_work():
    # 创建资源
    exchange_bg = create_exchange(EXCHANGE_NAME)
    exchange_queue = create_queue(QUEUE_NAME)
    create_binding(queue_name=exchange_queue, exchange_name=exchange_bg, routing_key=ROUTING_KEY)

    # consumer 消费消息
    consume_msg(QUEUE_NAME)


if __name__ == "__main__":
    invoke_background_work()
