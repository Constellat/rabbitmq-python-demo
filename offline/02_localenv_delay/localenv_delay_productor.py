#!/usr/bin/env python
from datetime import datetime
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
        header = {"x-delay": 60 * 1000}
        # message = amqp.Message(body=jsonutil.format_json({'a': 'UPDATE', 'v': {'login_time': 1, 'uid': 6}}),
        message = amqp.Message(body="HEELO WORLD!",
                               application_headers=header)
        ch.basic_publish(msg=message, exchange='niujianyu_test_offline_delay',
                         routing_key='niujianyu.test.delay')
        print(datetime.now())
        print(" [x] Sent %r" % message)
