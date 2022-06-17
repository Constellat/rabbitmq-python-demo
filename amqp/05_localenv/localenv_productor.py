#!/usr/bin/env python
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
        ch.basic_publish(amqp.Message('Hello World'), exchange='localenv_test_personal_njy',
                         routing_key='niujianyu.test.topic')
        print(" [x] Sent 'Hello World!'")
