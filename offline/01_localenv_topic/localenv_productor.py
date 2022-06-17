#!/usr/bin/env python
import amqp
# from mmsdk.common import jsonutil

if __name__ == "__main__":
    with amqp.Connection(
            host='10.16.0.11:5672',
            userid="maimai", password="maimai",
            virtual_host="/", confirm_publish=False,
            connect_timeout=3.0
    ) as conn:
        ch = conn.channel()
        # 第一条消息将只包含一个字符串Hello World！
        # msg = amqp.Message(body=jsonutil.format_json({'a': 'UPDATE', 'v': {'login_time': 1, 'uid': 5}}))
        msg = amqp.Message(body="HELLO WORLD!")
        ch.basic_publish(msg=msg, exchange='niujianyu_test_offline',
                         routing_key='niujianyu.test.topic')
        print(" [x] Sent %r" % msg)
