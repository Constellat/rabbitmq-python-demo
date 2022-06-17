#!/usr/bin/env python
from datetime import datetime
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
        header = {"x-delay": 60 * 1000}
        message = amqp.Message(body='Hello World', application_headers=header)
        ch.basic_publish(msg=message, exchange='test_delay', routing_key='test.delay')
        print(datetime.now())
        print(" [x] Sent %r" % message)
