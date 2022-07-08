#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/6/21 15:55
# @Author: niujianyu
# @File  : mq_connection.py

import pika

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
    # MQ 用户名和密码，默认都是guest
    credentials = pika.PlainCredentials(username, password)

    # 与 RabbitMQ 服务器建立连接
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host,
        port=port,
        virtual_host=virtual_host,
        credentials=credentials
    ))
    return connection
