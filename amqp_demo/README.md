# rabbitmq-python-demo

## amqp-demo

https://github.com/celery/py-amqp/

### 0. queue/exchange method

#### exchange

- `channel.exchange_delete(exchange=exchange_name)` 删除Exchange
- `channel.exchange_declare(exchange=exchange_name, type='direct')` 声明(新建)Exchange

#### queue

- `channel.queue_delete(queue=queue_name)` 删除队列
- `channel.queue_declare(queue=queue_name, auto_delete=False, durable=False)` 声明(新建)队列
- `channel.queue_purge(queue=queue_name)` 清空队列

#### binding

- `channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)`
    - 将exchange与queue绑定，有新消息，会copy一份发送到该队列
- `channel.queue_unbind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)` 
    - 队列解绑 参数和绑定完全一致

### 1. fanout

#### Code File

- `producer`: `amqp_demo/01_fanout/send.py`
- `consumer`: `amqp_demo/01_fanout/receive.py`

#### Code Running

1. `python amqp_demo/01_fanout/receive.py ` start consumer1
2. `python amqp_demo/01_fanout/receive.py ` start consumer2
3. start producer
    ```shell
    python amqp_demo/01_fanout/send.py First message.
    python amqp_demo/01_fanout/send.py Second message..
    python amqp_demo/01_fanout/send.py Third message...
    python amqp_demo/01_fanout/send.py Fourth message....
    python amqp_demo/01_fanout/send.py Fifth message.....
    ```

### 2. direct

#### Code File

- `producer`: `amqp_demo/02_direct/emit_log_direct.py`
- `consumer`: `amqp_demo/02_direct/receive_logs_direct.py`

#### Code Running

1. `python amqp_demo/02_direct/receive_logs_direct.py warning error` start consumer1
2. `python amqp_demo/02_direct/receive_logs_direct.py info warning error` start consumer2
3. start producer
    ```shell
    python amqp_demo/02_direct/emit_log_direct.py info "[INFO]: info message"
    python amqp_demo/02_direct/emit_log_direct.py warning "[WARN]: warning message"
    python amqp_demo/02_direct/emit_log_direct.py error "[ERROR]: error messsage"
    ```

### 3. topic

#### Code File

- `producer`: `amqp_demo/03_topic/emit_log_topic.py`
- `consumer`: `amqp_demo/03_topic/receive_logs_topic.py`

#### Code Running

1. `python amqp_demo/03_topic/receive_logs_topic.py "#" ` start consumer1
2. `python amqp_demo/03_topic/receive_logs_topic.py "kern.*" ` start consumer2
3. `python amqp_demo/03_topic/receive_logs_topic.py "*.critical" ` start consumer3
4. `python amqp_demo/03_topic/receive_logs_topic.py "kern.*" "*.critical" ` start consumer4
5. start producer
    ```shell
    python amqp_demo/03_topic/emit_log_topic.py "kern.critical" "A critical kern error"
    python amqp_demo/03_topic/emit_log_topic.py "kernel.critical" "A critical kernel error"
    python amqp_demo/03_topic/emit_log_topic.py "kern.info" "A kern info"
    python amqp_demo/03_topic/emit_log_topic.py "kernel.info" "A kernel info"
    ```

### 4. delay

#### Code File

- `producer`: `amqp_demo/04_delay/local_productor.py`
- `consumer`: `amqp_demo/04_delay/local_consumer.py`

#### Code Running

1. `python amqp_demo/04_delay/local_consumer.py ` start consumer
2. `python amqp_demo/04_delay/local_productor.py ` start producer

### 5. `basic_get`

#### Code File

- `basic_get`: `amqp_demo/05_basic_get/basic_get.py`
- `basic_consume`: `amqp_demo/05_basic_get/basic_consume.py`

#### Code Running

1. test basic_get `python amqp_demo/05_basic_get/basic_get.py `
2. type `CTRL+C` to stop the python process
3. test basic_consume `python amqp_demo/05_basic_get/basic_consume.py `
4. type `CTRL+C` to stop the python process

