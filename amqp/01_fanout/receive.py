#!/usr/bin/env python
import amqp

if __name__ == "__main__":
    with amqp.Connection(
            host='localhost',
            userid="admin", password="admin",
            virtual_host="/", confirm_publish=False,
            connect_timeout=3.0
    ) as conn:  # conn表示连接mq
        chan = conn.channel()  # chan 是开启的一个通道

        def on_message(message):
            print(" [x] Received %s" % message.body)
            print('Received message (delivery tag: {}): {}'.format(message.delivery_tag, message.body))
            chan.basic_ack(message.delivery_tag)

        # 消费一条消息，消费逻辑放在 on_message()
        chan.basic_consume(queue='test_fanout', callback=on_message)
        # result = chan.basic_get(queue='test_fanout', no_ack=False)
        while True:
            conn.drain_events()

