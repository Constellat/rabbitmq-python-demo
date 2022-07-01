# rabbitmq-python-demo

This is an example about how to use rabbit-mq in python!

how to connect rabbitmq by python?
> there are a few devtools helps.
> https://www.rabbitmq.com/devtools.html#python-dev

## pika_demo

this is an example about pika

the code is from RabbitMQ Tutorials.
https://rabbitmq.com/getstarted.html

### 1. "Hello World!"

- A program that sends messages is a producer :
  ![](./static/producer.png)
- This is how we represent a queue:
  ![](./static/queue.png)
- A consumer is a program that mostly waits to receive messages:
  ![](./static/consumer.png)

Our overall design will look like:
![](./static/python-one-overall.png)

#### Code File

- `producer`: `pika_demo/01_helloworld/receive.py`
- `consumer`: `pika_demo/01_helloworld/send.py`

#### Code Running

1. `python pika_demo/01_helloworld/receive.py` start consumer
2. `python pika_demo/01_helloworld/send.py` start producer

### 2. Work queues

If we need consume the message(only once every message) from one queue in multiple instances.

The overall design will look like:
![](./static/python-two.png)

the C1 and C2 construct the consumer group. A Message from a queue only consumed one times. It will be consumed in C1 or
C2.

#### Code File

- `producer`: `pika_demo/02_workqueue/new_task.py`
- `consumer`: `pika_demo/02_workqueue/worker.py`

#### Code Running

1. `python pika_demo/02_workqueue/worker.py` start consumer1
2. `python pika_demo/02_workqueue/worker.py` start consumer2
3. start producer
    ```shell
    python pika_demo/02_workqueue/new_task.py First message.
    python pika_demo/02_workqueue/new_task.py Second message..
    python pika_demo/02_workqueue/new_task.py Third message...
    python pika_demo/02_workqueue/new_task.py Fourth message....
    python pika_demo/02_workqueue/new_task.py Fifth message.....
    ```

### 3. Publish/Subscribe

If we need consume the same message in multiple instances.

The overall design will look like:
![](./static/python-three-overall.png)

the C1 and C2 is different consumer groups. A Message from exchange will be sent to two queues. And they will be
consumed both. A Message from a queue only consumed one times. C1 and C2 will consume the same message both.

#### Code File

- `producer`: `pika_demo/03_exchange/emit_log.py`
- `consumer`: `pika_demo/03_exchange/receive_logs.py`

#### Code Running

1. `python pika_demo/03_exchange/receive_logs.py` start consumer1
2. `python pika_demo/03_exchange/receive_logs.py` start consumer2
3. start producer
    ```shell
    python pika_demo/03_exchange/emit_log.py First message.
    python pika_demo/03_exchange/emit_log.py Second message..
    python pika_demo/03_exchange/emit_log.py Third message...
    python pika_demo/03_exchange/emit_log.py Fourth message....
    python pika_demo/03_exchange/emit_log.py Fifth message.....
    ```

### 4. Routing

If we need consume the specific part of the Messages, we need to change the using exchange and use routing_key to match.

The overall design will look like:
![](./static/direct-exchange.png)

the queue binding by the routing_key they needs. exchange will match routing_key and send the right to the matching
queues.

#### Code File

- `producer`: `pika_demo/04_routing/emit_log_direct.py`
- `consumer`: `pika_demo/04_routing/receive_logs_direct.py`

#### Code Running

1. `python pika_demo/04_routing/receive_logs_direct.py warning error` start consumer1
2. `python pika_demo/04_routing/receive_logs_direct.py info warning error` start consumer2
3. start producer
    ```shell
    python pika_demo/04_routing/emit_log_direct.py info "[INFO]: info message"
    python pika_demo/04_routing/emit_log_direct.py warning "[WARN]: warning message"
    python pika_demo/04_routing/emit_log_direct.py error "[ERROR]: error messsage"
    ```

### 5. Topics

If we want to fuzzy matching routing_key while binding between exchange and queue.

The overall design will look like:
![](./static/python-five.png)

It means the matching about routing_key supports fuzzy matching by wildcard. exchange will match routing_key and send
the right to the matching queues.

#### Code File

- `producer`: `pika_demo/05_topic/emit_log_topic.py`
- `consumer`: `pika_demo/05_topic/receive_logs_topic.py`

#### Code Running

1. `python pika_demo/05_topic/receive_logs_topic.py "#" ` start consumer1
2. `python pika_demo/05_topic/receive_logs_topic.py "kern.*" ` start consumer2
3. `python pika_demo/05_topic/receive_logs_topic.py "*.critical" ` start consumer3
4. `python pika_demo/05_topic/receive_logs_topic.py "kern.*" "*.critical" ` start consumer4
5. start producer
    ```shell
    python pika_demo/05_topic/emit_log_topic.py "kern.critical" "A critical kern error"
    python pika_demo/05_topic/emit_log_topic.py "kernel.critical" "A critical kernel error"
    python pika_demo/05_topic/emit_log_topic.py "kern.info" "A kern info"
    python pika_demo/05_topic/emit_log_topic.py "kernel.info" "A kernel info"
    ```

### 6. Rpc

If we want to achieve rpc invoke by rabbit-mq.

The overall design will look like:
![](./static/python-six.png)

It uses two queue to achieve the method parameters and the invoke result.

#### Code File

- `rpc-client`: `pika_demo/06_rpc/rpc_client.py`
- `rpc-server`: `pika_demo/06_rpc/rpc_server.py`

#### Code Running

1. `python pika_demo/06_rpc/rpc_server.py ` start rpc-server
2. `python pika_demo/06_rpc/rpc_client.py ` start rpc-client

### 7. delay

If we want to use delay-message(Consumer get the message after producing for a while).

The message and exchange also supports the matching role above.

#### Code File

- `producer`: `pika_demo/07_delay/local_productor.py`
- `consumer`: `pika_demo/07_delay/local_consumer.py`

#### Code Running

1. `python pika_demo/07_delay/local_consumer.py ` start consumer
2. `python pika_demo/07_delay/local_productor.py ` start producer
