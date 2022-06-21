# coding=utf-8

__company__ = 'taou'
__author__ = 'zhanglei'

import json
import amqp

RABBIT_HOST = "localhost"
RABBIT_TCP_PORT = 5672
RABBIT_USER = "admin"
RABBIT_PASSWORD = "admin"
VIRTUAL_HOST = "/"
conn = None


def get_rabbit_chan():
    global conn
    if not conn or not conn.connected:
        conn = amqp.Connection(host="%s:%s" % (RABBIT_HOST, RABBIT_TCP_PORT), userid=RABBIT_USER,
                               password=RABBIT_PASSWORD,
                               virtual_host=VIRTUAL_HOST)
    chan = conn.channel()
    return chan


def create_queue(name, auto_delete=False, durable=True, exclusive=False, arguments=None):
    queue_name = name
    chan = get_rabbit_chan()
    chan.queue_delete(queue=queue_name)
    chan.queue_declare(queue=queue_name, auto_delete=auto_delete, durable=durable, exclusive=exclusive,
                       arguments=arguments)
    chan.queue_purge(queue=queue_name)
    return queue_name


def create_exchange(name, change_type='fanout', auto_delete=False, durable=True, arguments=None):
    exchange_name = name
    chan = get_rabbit_chan()
    chan.exchange_delete(exchange=exchange_name)
    chan.exchange_declare(
        exchange=exchange_name, auto_delete=auto_delete, type=change_type, durable=durable, arguments=arguments)
    return exchange_name


def create_binding(queue_name, exchange_name, routing_key=''):
    chan = get_rabbit_chan()
    chan.queue_bind(queue=queue_name, exchange=exchange_name, routing_key=routing_key)


def get_msg(queue):
    chan = get_rabbit_chan()
    msg = chan.basic_get(queue=queue)
    if msg:
        print(msg, msg.delivery_info)
        chan.basic_ack(delivery_tag=msg.delivery_info['delivery_tag'])
    else:
        print("msg ttl")
    return msg


def send_msg(msg, exchange_name='', routing_key='', **kwargs):
    chan = get_rabbit_chan()
    msg = amqp.Message(body=json.dumps(msg), **kwargs)
    chan.basic_publish(exchange=exchange_name, routing_key=routing_key, msg=msg)


# fanout exchange 广播形式，忽略 routing_key
def test_fanout_exchange():
    exchange_name = create_exchange('test_fanout_exchange_flow', change_type='fanout')
    queue1 = create_queue('test_fanout_exchange_flow1')
    queue2 = create_queue('test_fanout_exchange_flow2')
    create_binding(queue_name=queue1, exchange_name=exchange_name)
    create_binding(queue_name=queue2, exchange_name=exchange_name, routing_key='test_routing_key')

    send_msg(msg='test', exchange_name=exchange_name, routing_key='test_routing_key')


# 完全匹配 routing_key
def test_direct_exchange():
    exchange_name = create_exchange('test_direct_exchange_flow', change_type='direct')
    queue1 = create_queue('test_direct_exchange_flow1')
    queue2 = create_queue('test_direct_exchange_flow2')
    create_binding(queue_name=queue1, exchange_name=exchange_name)
    create_binding(queue_name=queue2, exchange_name=exchange_name, routing_key='test_routing_key')

    queue3 = create_queue('test_direct_exchange_flow3')
    create_binding(queue_name=queue3, exchange_name=exchange_name, routing_key='test_routing_key')

    send_msg(msg='test', exchange_name=exchange_name, routing_key='test_routing_key')
    # send_msg(msg='test', exchange_name=exchange_name, routing_key='test_routing_key_test')
    # send_msg(msg='test', exchange_name=exchange_name)


# 模糊匹配 routing_key
def test_topic_exchange():
    exchange_name = create_exchange('test_topic_exchange_flow', change_type='direct')
    # queue1 = create_queue('test_topic_exchange_flow1')
    # queue2 = create_queue('test_topic_exchange_flow2')
    # create_binding(queue_name=queue1, exchange_name=exchange_name)
    # create_binding(queue_name=queue2, exchange_name=exchange_name, routing_key='test_routing_key')

    queue3 = create_queue('test_topic_exchange_flow3')
    create_binding(queue_name=queue3, exchange_name=exchange_name, routing_key='*routing_key*')

    send_msg(msg='test', exchange_name=exchange_name, routing_key='test_routing_key')
    send_msg(msg='test', exchange_name=exchange_name, routing_key='test_routing_key_test')
    send_msg(msg='test', exchange_name=exchange_name)


# 不指定 exchange，消息会被投递到 routingkey 对应的 queue 上
def test_default_exchange():
    # 普通消息
    queue_name = create_queue('test_default_exchange_flow')
    send_msg(msg='test_default_exchange', routing_key=queue_name)


def test_ttl_msg_queue():
    queue_name = create_queue('test_ttl_queue_flow', arguments={'x-message-ttl': 20 * 1000})
    send_msg(msg='test_default_exchange', routing_key=queue_name)

    no_ttl_queue_name = create_queue('test_no_ttl_queue_flow')
    send_msg(msg='test_default_exchange', routing_key=no_ttl_queue_name, expiration='120000')
    send_msg(msg='test_default_exchange', routing_key=no_ttl_queue_name)


def test_delay_msg_queue():
    test_delay_msg_exchange = create_exchange(
        'test_delay_msg_queue', change_type='x-delayed-message', arguments={'x-delayed-type': 'fanout'})
    queue_name = create_queue('test_delay_msg_queue')
    create_binding(queue_name=queue_name, exchange_name=test_delay_msg_exchange)
    header = {'x-delay': 10 * 1000}
    send_msg(
        msg='test_default_exchange', exchange_name=test_delay_msg_exchange, application_headers=header)


def test_dead_letter_queue():
    # test for ttl message in dead_letter_exchange
    dead_letter_exchange = create_exchange('dead_letter_exchange')
    dead_letter_queue_ttl = create_queue('dead_letter_queue_ttl', arguments={})
    dead_queue_ttl = create_queue(name='ttl_queue', arguments={
        'x-dead-letter-exchange': dead_letter_exchange,
        'x-dead-letter-routing-key': dead_letter_queue_ttl,
        'x-message-ttl': 10 * 1000
    })
    create_binding(queue_name=dead_letter_queue_ttl, exchange_name=dead_letter_exchange,
                   routing_key=dead_letter_queue_ttl)

    send_msg(msg='test_default_exchange', exchange_name="", routing_key=dead_queue_ttl)

    # test for max_length_capacity message in dead_letter_exchange
    dead_letter_queue_capacity = create_queue('dead_letter_queue_capacity', arguments={})
    min_capacity_queue = create_queue(name='min_capacity_queue', arguments={
        'x-dead-letter-exchange': dead_letter_exchange,
        'x-dead-letter-routing-key': dead_letter_queue_capacity,
        'x-max-length': 1
    })
    create_binding(queue_name=dead_letter_queue_capacity, exchange_name=dead_letter_exchange, routing_key=dead_letter_queue_capacity)


    send_msg(msg='test_default_exchange', exchange_name='', routing_key=min_capacity_queue)
    send_msg(msg='test_default_exchange', exchange_name='', routing_key=min_capacity_queue)

    chan = get_rabbit_chan()
    msg = chan.basic_get(queue=min_capacity_queue)
    chan.basic_reject(delivery_tag=msg.delivery_info['delivery_tag'], requeue=0)


def test_priority_queue():
    priority_queue = create_queue(name='priority_queue', arguments={'x-max-priority': 10})
    send_msg(msg='test_priority_1', routing_key=priority_queue, priority=1)
    send_msg(msg='test_priority_5', routing_key=priority_queue, priority=5)
    send_msg(msg='test_priority_8', routing_key=priority_queue, priority=8)
    send_msg(msg='test_priority_3', routing_key=priority_queue, priority=3)

    print(get_msg(priority_queue).body)
    print(get_msg(priority_queue).body)
    print(get_msg(priority_queue).body)
    print(get_msg(priority_queue).body)


def test_durable():
    durable_exchange = create_exchange('durable_exchange')
    transient_exchange = create_exchange('transient_exchange', durable=False)

    durable_queue = create_queue(name='durable_queue', arguments={'x-max-priority': 10})
    transient_queue = create_queue(name='transient_queue', arguments={'x-max-priority': 10}, durable=False)

    create_binding(durable_queue, durable_exchange)
    create_binding(durable_queue, transient_exchange)
    create_binding(transient_queue, durable_exchange)
    create_binding(transient_queue, transient_exchange)

    send_msg(msg='test_priority_3', exchange_name=durable_exchange)
    send_msg(msg='test_priority_3', exchange_name=transient_exchange)

    send_msg(msg='test_priority_3', exchange_name=durable_exchange, delivery_mode=2)


def clear_all():
    import requests

    def delete(names, is_queue=True):
        chan = get_rabbit_chan()

        if is_queue:
            func = chan.queue_delete
        else:
            func = chan.exchange_delete

        for name in names:
            func(name)

    url = 'http://maimai:maimai@10.11.60.59:15672/api/queues/'
    ret = requests.get(url=url)
    queue_names = [r['name'] for r in ret.json() if r.get('name', '') and 'amq' not in r.get('name', '')]
    delete(queue_names, is_queue=True)

    url = 'http://maimai:maimai@10.11.60.59:15672/api/exchanges/'
    ret = requests.get(url=url)
    exchange_names = [r['name'] for r in ret.json() if r.get('name', '') and 'amq' not in r.get('name', '')]
    delete(exchange_names, is_queue=False)


if __name__ == "__main__":
    # clear_all()
    # test_fanout_exchange()
    # test_direct_exchange()
    # test_topic_exchange()
    # test_default_exchange()
    # test_delay_msg_queue()
    # test_ttl_msg_queue()
    # test_priority_queue()
    test_dead_letter_queue()
    # test_durable()
    pass
