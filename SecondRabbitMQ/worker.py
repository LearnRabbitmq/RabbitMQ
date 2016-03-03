#coding:utf-8

import pika
import time

credentials = pika.PlainCredentials('admin','admin123')
parmters = pika.ConnectionParameters('192.168.10.154',5672,
                                     'my_vhost',credentials)
connection = pika.BlockingConnection(parmters)

channel = connection.channel()
# 虽然有了消息反馈机制，但是如果rabbitmq自身挂掉的话，那么任务还是会丢失。所以需要将任务持久化存储起来。声明持久化存储：
# 但是这个程序会执行错误，因为hello这个队列已经存在，并且是非持久化的，rabbitmq不允许使用不同的参数来重新定义存在的队列。重新定义一个队列：
"""
持久化三要素：
a) 将交换机设成 durable。
b) 将队列设成 durable。
c) 将消息的 Delivery Mode 设置成2 。
"""
channel.queue_declare(queue = 'hello', durable = True)


def callback(ch,method,properties,body):
    print '[x] Recived %s' %(body)
    time.sleep(5)
    print '[x] Done'


# 如果一个工作者，在处理任务的时候挂掉，
# 这个任务就没有完成，应当交由其他工作者处理。所以应当有一种机制，当一个工作者完成任务时，会反馈消息
# 消息确认就是当工作者完成任务后，会反馈给rabbitmq
    ch.basic_ack(delivery_tag = method.delivery_tag)

# 公平调度(Fair dispatch)
"""
上面实例中，虽然每个工作者是依次分配到任务，但是每个任务不一定一样。可能有的任务比较重，执行时间比较久；
有的任务比较轻，执行时间比较短。如果能公平调度就最好了，使用basic_qos设置prefetch_count=1，
使得rabbitmq不会在同一时间给工作者分配多个任务，即只有工作者完成任务之后，才会再次接收到任务。
"""
channel.basic_qos(prefetch_count=1)
  
# 去除no_ack=True参数或者设置为False也可以。    
# 用这个代码运行，即使其中一个工作者ctrl+c退出后，正在执行的任务也不会丢失，rabbitmq会将任务重新分配给其他工作者
channel.basic_consume(callback, queue = 'hello', no_ack = False)

channel.start_consuming()