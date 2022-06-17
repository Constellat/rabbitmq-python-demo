#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/6/6 17:29
# @Author: niujianyu
# @File  : add_background_work.py
__company__ = 'taou'
__author__ = 'zhanglei'

import json
from six.moves import cPickle
import amqp
RABBIT_HOST = "localhost"
RABBIT_TCP_PORT = 5672
RABBIT_USER = "admin"
RABBIT_PASSWORD = "admin"
VIRTUAL_HOST = "/"
conn = None


def get_rabbit_chan():
    global conn
    if not conn or not conn.connected:
        conn = amqp.Connection(host="%s:%s" % (RABBIT_HOST, RABBIT_TCP_PORT), userid=RABBIT_USER,
                               password=RABBIT_PASSWORD,
                               virtual_host=VIRTUAL_HOST)
    chan = conn.channel()
    return chan


def create_queue(name, auto_delete=False, durable=True, exclusive=False, arguments=None):
    queue_name = name
    chan = get_rabbit_chan()
    chan.queue_delete(queue=queue_name)
    chan.queue_declare(
        queue=queue_name, auto_delete=auto_delete, durable=durable, exclusive=exclusive, arguments=arguments)
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


def get_msg(queue):
    chan = get_rabbit_chan()
    msg = chan.basic_get(queue=queue)
    if msg:
        chan.basic_ack(delivery_tag=msg.delivery_info['delivery_tag'])
    else:
        print("msg ttl")
    return msg


def send_msg(msg, exchange_name='', routing_key='', **kwargs):
    chan = get_rabbit_chan()
    msg = amqp.Message(body=msg, **kwargs)
    chan.basic_publish(exchange=exchange_name, routing_key=routing_key, msg=msg)


def bg_function(a, b):
    print("bg_function print: {} {}".format(a, b))


class MyMessage:
    def __init__(self, func_name, class_name, module_path, kwargs):
        self.func_name = func_name
        self.class_name = class_name
        self.module_path = module_path
        self.kwargs = kwargs


def build_function_type_msg(func, kwargs):
    func_name = func.__name__
    import inspect, os
    module_path = str(os.path.basename(inspect.getmodule(func).__file__)).split('.')[0]
    kwargs = kwargs
    class_name = func.__module__

    msg = MyMessage(func_name, class_name, module_path, kwargs)
    return cPickle.dumps(msg, protocol=2)

def build_class_method_type_msg(func, kwargs):
    func_name = func.__name__
    class_name = func.__qualname__.split('.')[0]
    import inspect, os
    module_path = str(os.path.basename(inspect.getmodule(func).__file__)).split('.')[0]
    kwargs = kwargs

    msg = MyMessage(func_name, class_name, module_path, kwargs)
    object_str = cPickle.dumps(msg, protocol=2)
    return object_str


def add_background_work(func, consumer_p, **kwargs):
    print("type: %s" % (type(func)))
    from types import FunctionType, MethodType
    # 创建资源
    exchange_bg = create_exchange('test_exchange_bg')
    exchange_queue = create_queue('test_exchange_bg')
    create_binding(queue_name=exchange_queue, exchange_name=exchange_bg, routing_key=exchange_queue)

    if isinstance(func, FunctionType):
        msg = build_function_type_msg(func=func, kwargs=kwargs)
    elif isinstance(func, MethodType):
        msg = build_class_method_type_msg(func=func, kwargs=kwargs)
    else:
        raise Exception('func type error')

    # producer 生产消息
    send_msg(msg, exchange_name=exchange_bg)

    # consumer 消费
    msg = get_msg(queue=exchange_queue)
    if not msg:
        raise Exception('no msg')

    # 消费者处理消息
    myMessage = cPickle.loads(msg.body)
    consumer_p(myMessage)


def consumer_process_class(myMessage):
    class_name = myMessage.class_name
    func_name = myMessage.func_name
    module_path = myMessage.module_path
    kwargs = myMessage.kwargs
    import importlib
    print('类名字：%s，函数名字:%s, 包路径:%s, 函数参数:%s' % (class_name, func_name, module_path, kwargs))

    module = importlib.import_module(module_path)
    if class_name:
        cls = getattr(module, class_name)
        print(type(cls))
        func = getattr(cls, func_name)
        print(type(func))
        func(**kwargs)
    else:
        func = getattr(module, func_name)
        print(type(func))
        func(**kwargs)


def consumer_process_function(func_name, module_path, kwargs):
    import importlib
    print("函数名字:%s, 包路径:%s, 函数参数:%s" % (func_name, module_path, kwargs))
    bg_module = importlib.import_module(module_path)
    func = getattr(bg_module, func_name)
    func(**kwargs)


class BgTest(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def print_bg_test(self, c):
        print("class_type_bg_test print: {} {} {}".format(self.a, self.b, c))

    def print_bg_test_2(self, c):
        print("class_type_bg_test print: {}".format(c))

    @classmethod
    def print_bg_test_3(cls, c):
        print("class method class_type_bg_test print: {}".format(c))

    def test_bg_class_method(self):
        add_background_work(func=self.print_bg_test_3, consumer_p=consumer_process_class, c='test_bg_class_method')

    def test_bg_2(self):
        add_background_work(func=self.print_bg_test_2, consumer_p=consumer_process_class, c='test_bg_2', self=self)

    def test_bg(self):
        add_background_work(func=self.print_bg_test, consumer_p=consumer_process_class, c='test_bg', self=self)


def test_bg_class_instance():
    xx = BgTest(a='test_bg_class_instance', b='111111')
    xx.test_bg()


def test_bg_class_instance_2():
    xx = BgTest(a='test_bg_class_instance_2', b='222222')
    xx.test_bg_2()


def test_bg_class_class_method():
    xx = BgTest(a='test_bg_class_class_method', b='class_method')
    xx.test_bg_class_method()


def clear_all():
    import requests

    def delete(names, is_queue=True):
        chan = get_rabbit_chan()

        if is_queue:
            func = chan.queue_delete
        else:
            func = chan.exchange_delete

        for name in names:
            func(name)

    url = 'http://maimai:maimai@10.11.60.59:15672/api/queues/'
    ret = requests.get(url=url)
    queue_names = [r['name'] for r in ret.json() if r.get('name', '') and 'amq' not in r.get('name', '')]
    delete(queue_names, is_queue=True)

    url = 'http://maimai:maimai@10.11.60.59:15672/api/exchanges/'
    ret = requests.get(url=url)
    exchange_names = [r['name'] for r in ret.json() if r.get('name', '') and 'amq' not in r.get('name', '')]
    delete(exchange_names, is_queue=False)


if __name__ == "__main__":
    # clear_all()
    # add_background_work(func=bg_function, consumer_p=consumer_process_function, a='aaaaa', b='bbbbb')
    # test_bg_class_instance_2()
    # test_bg_class_instance()
    # 不支持静态方法？没有实际的对象
    test_bg_class_class_method()
    pass