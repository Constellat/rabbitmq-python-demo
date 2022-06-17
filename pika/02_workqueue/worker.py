#!/usr/bin/env python
# 您需要打开三个控制台。两个将运行worker.py 脚本。
# 这些控制台将是我们的两个消费者 C1 和 C2。

import pika, sys, os, time

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
    # durable 将其声明为耐用的：即使 RabbitMQ 重新启动，队列也不会丢失
    channel.queue_declare(queue= 'task_queue', durable= True)

    # 将回调函数订阅到队列来工作。
    # 每当我们收到消息时，Pika 库都会调用此回调函数
    # 单个queue消费的消息是单线程的？所以有序的？
    # 多个程序启动，监听的一个queue，一个queue只会有一个标志位表示消费位点，确保消息不会重复。如何确保消息负载均衡？
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        time.sleep((body.count(b'.') % 2)*10)
        print(" [x] Done")
        # 这行代码手动确定消费完成，在这之前中断的消息消费会在另外的消费者上重新消费
        # 漏写basic_ack是一个常见的错误。这是一个简单的错误，但后果很严重。
        # 当您的消费者退出时，所有已经消费过的消息将被重新传递（这可能看起来像随机重新传递），
        # 但是 RabbitMQ 将消耗越来越多的内存，因为它无法释放任何未确认的消息。
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # 使用带有prefetch_count=1 设置的Channel#basic_qos通道方法
    # 确认消费者已消费消息才会发新消息
    channel.basic_qos(prefetch_count=1)

    # 我们需要告诉 RabbitMQ 这个特定的回调函数应该从我们的hello队列中接收消息
    # auto_ack 默认为False，所以默认下是确定Consumer正常消费后才会移动消费位点
    channel.basic_consume(queue='task_queue',
                          # auto_ack=True,
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

