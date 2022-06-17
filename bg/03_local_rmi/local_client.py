#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/6/10 15:03
# @Author: niujianyu
# @File  : local_client.py
import amqp
import re, inspect, os
from six.moves import cPickle
from bg.data_object.DataObject import DataObject
from bg.data_object.InnerObject import InnerObject
from bg.data_object.MyMessage import MyMessage

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


def get_module_path(func):
    _MODULE_PATTERN = re.compile('^bg')
    if _MODULE_PATTERN.search(func.__module__):
        return func.__module__
    module_path_list = str(os.path.dirname(inspect.getmodule(func).__file__)).split('/')[::-1]
    paths2 = []
    for p in module_path_list:
        paths2.append(p)
        if p == "bg":
            break
    return '.'.join(paths2[::-1]) + '.' + func.__module__


def build_class_method_type_msg(func, kwargs):
    func_name = func.__name__
    class_name = func.__qualname__.split('.')[0]
    module_path = get_module_path(func)
    kwargs = kwargs

    msg = MyMessage(func_name, class_name, module_path, kwargs)
    object_str = cPickle.dumps(msg, protocol=2)
    return object_str


def send_msg(msg, exchange_name, routing_key):
    chan = get_rabbit_chan()
    chan.basic_publish(amqp.Message(msg), exchange=exchange_name, routing_key=routing_key)


def add_background_work(func, **kwargs):
    # 构建消息
    msg = build_class_method_type_msg(func=func, kwargs=kwargs)

    # producer 生产消息
    send_msg(msg, EXCHANGE_NAME, ROUTING_KEY)


if __name__ == "__main__":
    inner_object = InnerObject()
    data_object = DataObject("local_client", inner_object)
    add_background_work(func=data_object.test_bg1, self=data_object, inner_object=inner_object)
    print(" [x] Sent RMI Task Done")
