#!/usr/bin/env python
from datetime import datetime
import amqp

if __name__ == "__main__":
    with amqp.Connection(
            host='10.16.0.11:5672',
            userid="maimai", password="maimai",
            virtual_host="/", confirm_publish=False,
            connect_timeout=3.0
    ) as conn:
        ch = conn.channel()
        # 第一条消息将只包含一个字符串Hello World！
        header = {"x-delay": 60 * 1000}
        message = amqp.Message(body='Hello World', application_headers=header)
        ch.basic_publish(msg=message, exchange='niujianyu_test_delay',
                         routing_key='niujianyu.test.delay')
        print(datetime.now())
        print(" [x] Sent 'Hello World!'")
