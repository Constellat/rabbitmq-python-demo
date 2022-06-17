#!/usr/bin/env python
import pika, sys

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
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# 在 RabbitMQ 中，消息永远不能直接发送到队列，它总是需要经过一个交换。
# 队列名称需要在routing_key参数中指定
routing_key = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
# 找到对应的exchange，并让其使用routing_key来找到绑定的queue并推送消息
channel.basic_publish(exchange='direct_logs', routing_key=routing_key, body=message)
print(" [x] Sent %r" % message)

# 关闭连接
connection.close()
