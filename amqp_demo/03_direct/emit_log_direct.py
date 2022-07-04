#!/usr/bin/env python
import sys, os
import amqp

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from amqp_demo._base import mq_connection


def main():
    conn = mq_connection.get_mq_connection()
    channel = conn.channel()

    channel.exchange_declare(exchange='direct_logs', type='direct', auto_delete=False)

    routing_key = sys.argv[1] if len(sys.argv) > 1 else 'info'
    message_body = ' '.join(sys.argv[2:]) or 'Hello World!'

    message = amqp.Message(message_body)
    channel.basic_publish(msg=message, exchange='direct_logs', routing_key=routing_key)
    print(" [x] Sent %s" % message.body)

    channel.close()
    conn.close()


if __name__ == '__main__':
    main()


