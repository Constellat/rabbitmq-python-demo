#!/usr/bin/env python
# 您需要打开三个控制台。两个将运行worker.py 脚本。
# 这些控制台将是我们的两个消费者 C1 和 C2。

import amqp

EXCHANGE_NAME = 'logs'


if __name__ == "__main__":
    with amqp.Connection(
            host='localhost',
            userid="admin", password="admin",
            virtual_host="/", confirm_publish=False,
            connect_timeout=3.0
    ) as conn:  # conn表示连接mq
        chan = conn.channel()  # chan 是开启的一个通道
        chan.exchange_declare(exchange=EXCHANGE_NAME, type='fanout', auto_delete=False, durable=True)
        # 给空 会默认给一个queue_name
        result = chan.queue_declare(
            queue="", durable=True, exclusive=True)
        queue_name = result.queue
        chan.queue_bind(queue=queue_name, exchange=EXCHANGE_NAME, routing_key='')
        # 清除队列
        chan.queue_purge(queue=queue_name)


        def on_message(message):
            print(" [x] Received %s: %s" % (message.delivery_info.get('routing_key'), message.body))
            print('Received message (delivery tag: {}): {}'.format(message.delivery_tag, message.body))
            print(" [x] Done")

            chan.basic_ack(message.delivery_tag)

        # 消费一条消息，消费逻辑放在 on_message()
        # result = chan.basic_get(queue='test_fanout', no_ack=False)
        chan.basic_consume(queue=queue_name, callback=on_message)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        while True:
            conn.drain_events()
