#!/usr/bin/env python
import amqp

if __name__ == "__main__":
    with amqp.Connection(
            host='localhost',
            userid="admin", password="admin",
            virtual_host="/", confirm_publish=False,
            connect_timeout=3.0
    ) as conn:
        ch = conn.channel()
        # 第一条消息将只包含一个字符串Hello World！
        ch.basic_publish(amqp.Message('Hello World'), exchange='test_direct', routing_key='test.direct')
        print(" [x] Sent 'Hello World!'")
