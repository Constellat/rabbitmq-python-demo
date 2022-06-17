#!/usr/bin/env python
from datetime import datetime
import amqp

if __name__ == "__main__":
    with amqp.Connection(
            host='10.16.0.11:5672',
            userid="maimai", password="maimai",
            virtual_host="/", confirm_publish=False,
            connect_timeout=3.0
    ) as conn:  # conn表示连接mq
        chan = conn.channel()  # chan 是开启的一个通道


        def on_message(message):
            print(" [x] Received %s: %s" % (message.delivery_info.get('routing_key'), message.body))
            print('Received message (delivery tag: {}): {}'.format(message.delivery_tag, message.body))
            print(message.properties.get('application_headers', {}))
            print(datetime.now())
            print(" [x] Done")

            chan.basic_ack(message.delivery_tag)


        # 消费一条消息，消费逻辑放在 on_message()
        # result = chan.basic_get(queue='test_fanout', no_ack=False)
        chan.basic_consume(queue='niujianyu_test_delay', callback=on_message)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        while True:
            conn.drain_events()
