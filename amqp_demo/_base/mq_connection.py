#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/6/21 15:55
# @Author: niujianyu
# @File  : mq_connection.py

import amqp

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 5672
DEFAULT_VIRTUAL_HOST = '/'
DEFAULT_USERNAME = 'admin'
DEFAULT_PASSWORD = 'admin'


def get_mq_connection(host=DEFAULT_HOST,
                      port=DEFAULT_PORT,
                      virtual_host=DEFAULT_VIRTUAL_HOST,
                      username=DEFAULT_USERNAME,
                      password=DEFAULT_PASSWORD):
    # 与 RabbitMQ 服务器建立连接
    connection = amqp.Connection(
        host="%s:%s" % (host, port),
        userid=username,
        password=password,
        virtual_host=virtual_host,
        confirm_publish=False,
        connect_timeout=3.0
    )
    return connection
