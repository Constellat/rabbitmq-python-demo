#!/usr/bin/env python
# 您需要打开三个控制台。两个将运行worker.py 脚本。
# 这些控制台将是我们的两个消费者 C1 和 C2。

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
            print(message.body)
            print(" [x] Done")

            chan.basic_ack(message.delivery_tag)


        # 消费一条消息，消费逻辑放在 on_message()
        # result = chan.basic_get(queue='test_fanout', no_ack=False)
        chan.basic_consume(queue='niujianyu_test_bgjobs', callback=on_message)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        while True:
            conn.drain_events()
