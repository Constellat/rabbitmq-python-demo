#!/usr/bin/env python
import pika, sys, os

def main():
    # MQ 用户名和密码，默认都是guest
    credentials = pika.PlainCredentials('admin', 'admin')

    # 与 RabbitMQ 服务器建立连接
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost',
        port=5672,
        virtual_host='/',
        credentials=credentials
    ))

    channel = connection.channel()

    # 如果我们确定队列已经存在，我们可以避免这种情况。
    # 例如，如果send.py程序之前运行过。
    # 但是我们还不确定首先运行哪个程序。在这种情况下，最好在两个程序中重复声明队列。
    channel.queue_declare(queue= 'hello' )

    # 将回调函数订阅到队列来工作。
    # 每当我们收到消息时，Pika 库都会调用此回调函数
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    # 我们需要告诉 RabbitMQ 这个特定的回调函数应该从我们的hello队列中接收消息
    channel.basic_consume(queue='hello',
                          auto_ack=True,
                          on_message_callback=callback)


    print(' [*] Waiting for messages. To exit press CTRL+C')
    # 我们进入一个永无止境的循环，等待数据并在必要时运行回调
    channel.start_consuming()

# 最后，在程序关闭期间捕获KeyboardInterrupt。
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


