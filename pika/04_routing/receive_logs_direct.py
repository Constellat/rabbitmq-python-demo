#!/usr/bin/env python
# 您需要打开三个控制台。两个将运行worker.py 脚本。
# 这些控制台将是我们的两个消费者 C1 和 C2。

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

    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    # queue=''  让服务器为我们选择一个随机队列名称
    # 此时result.method.queue包含一个随机队列名称。
    # 一旦消费者连接关闭，队列应该被删除。
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    print(queue_name)

    severities = sys.argv[1:]
    if not severities:
        sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
        sys.exit(1)

    for severity in severities:
        # 绑定是exchange和queue之间的关系。这可以简单地理解为：queue对来自此exchange的消息感兴趣
        # 绑定可以采用额外的routing_key参数。为了避免与basic_publish参数混淆，我们将其称为 绑定键。
        # 将queue绑定到exchange的每一个routing_key下
        channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)
        # 队列解绑 参数和绑定完全一致
        # channel.queue_unbind(exchange='direct_logs', queue=queue_name, routing_key=severity)

    # 将回调函数订阅到队列来工作。
    # 每当我们收到消息时，Pika 库都会调用此回调函数
    # 单个queue消费的消息是单线程的？所以有序的？
    # 多个程序启动，监听的一个queue，一个queue只会有一个标志位表示消费位点，确保消息不会重复。如何确保消息负载均衡？
    def callback(ch, method, properties, body):
        print(" [x] Received %r:%r" % (method.routing_key, body))
        print(" [x] Done")
        # 这行代码手动确定消费完成，在这之前中断的消息消费会在另外的消费者上重新消费
        # 漏写basic_ack是一个常见的错误。这是一个简单的错误，但后果很严重。
        # 当您的消费者退出时，所有已经消费过的消息将被重新传递（这可能看起来像随机重新传递），
        # 但是 RabbitMQ 将消耗越来越多的内存，因为它无法释放任何未确认的消息。
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # 使用带有prefetch_count=1设置的Channel#basic_qos通道方法
    # 告诉 RabbitMQ 一次不要给一个 worker 多个消息。
    # 或者，换句话说，在工作人员处理并确认之前的消息之前，不要向工作人员发送新消息。
    # 相反，它将把它分派给下一个不忙的工人。
    # channel.basic_qos(prefetch_count=1)

    # 我们需要告诉 RabbitMQ 这个特定的回调函数应该从我们的hello队列中接收消息
    # auto_ack 默认为False，所以默认下是确定Consumer正常消费后才会移动消费位点
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

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
