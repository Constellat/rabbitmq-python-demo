#!/usr/bin/env python
import amqp

EXCHANGE_NAME = 'logs'

if __name__ == "__main__":
    with amqp.Connection(
            host='localhost',
            userid="admin", password="admin",
            virtual_host="/", confirm_publish=False,
            connect_timeout=3.0
    ) as conn:
        ch = conn.channel()
        ch.exchange_declare(exchange=EXCHANGE_NAME, type='fanout', auto_delete=False, durable=True)

        # 第一条消息将只包含一个字符串Hello World！
        msg = 'Hello World!'
        ch.basic_publish(amqp.Message(msg), exchange=EXCHANGE_NAME, routing_key='test.topic')
        print(" [x] Sent: '%s'" % msg)
