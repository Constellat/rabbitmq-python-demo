#!/usr/bin/env python
from datetime import datetime
import pika

# MQ 用户名和密码，默认都是guest
credentials = pika.PlainCredentials('admin', 'admin')

# 与 RabbitMQ 服务器建立连接
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost',
    port=5672,
    virtual_host='/',
    credentials=credentials
))
channel = connection.channel()

# 配置exchange 支持通过routing_key来配置绑定关系
arguments = {"x-delayed-type": "direct"}
channel.exchange_declare(exchange='delayed_exchange', exchange_type='x-delayed-message', arguments=arguments)

message = 'Hello World!'
# 找到对应的exchange，并让其使用routing_key来找到绑定的queue并推送消息
property = pika.BasicProperties(headers={"x-delay": 2*60*1000})
channel.basic_publish(exchange='delayed_exchange', routing_key="routing_key", body=message, properties=property)
print(datetime.now())
print(" [x] Sent %r" % message)

# 关闭连接
connection.close()
