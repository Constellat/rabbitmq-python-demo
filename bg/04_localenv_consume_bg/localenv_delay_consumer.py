#!/usr/bin/env python
import amqp
from six.moves import cPickle

RABBIT_HOST = "10.16.0.11"
RABBIT_TCP_PORT = 5672
RABBIT_USER = "maimai"
RABBIT_PASSWORD = "maimai"
VIRTUAL_HOST = "/"


if __name__ == "__main__":
    with amqp.Connection(
            host="%s:%s" % (RABBIT_HOST, RABBIT_TCP_PORT),
            userid=RABBIT_USER, password=RABBIT_PASSWORD,
            virtual_host=VIRTUAL_HOST, confirm_publish=False,
            connect_timeout=3.0
    ) as conn:  # conn表示连接mq
        chan = conn.channel()  # chan 是开启的一个通道


        def on_message(message):
            print(" [x] Received %s: %s" % (message.delivery_info.get('routing_key'), message.body))
            print('Received message (delivery tag: {}): {}'.format(message.delivery_tag, message.body))
            body = cPickle.loads(message.body)

            print(" [x] Done")

            chan.basic_ack(message.delivery_tag)


        # 消费一条消息，消费逻辑放在 on_message()
        # result = chan.basic_get(queue='test_fanout', no_ack=False)
        chan.basic_consume(queue='localenv_test_personal_njy', callback=on_message)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        while True:
            conn.drain_events()
