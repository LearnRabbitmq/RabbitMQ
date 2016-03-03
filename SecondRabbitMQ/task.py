#coding:utf-8
"""
消息发送者可以理解为任务分配者，消息接收者可以理解为工作者，
当工作者接收到一个任务，还没完成的时候，任务分配者又发一个任务过来，
那就忙不过来了，于是就需要多个工作者来共同处理这些任务，这些工作者，就称为工作队列

队列就是传递消息的载体，消息必须放到队列中。如何放到队列中，需要交换机bangding，路由规则
消息的属性：routeing key
"""
import pika
import sys


credentials = pika.PlainCredentials('admin','admin123')
parmters = pika.ConnectionParameters('192.168.10.154',
                                    5672,'my_vhost',credentials)

connection = pika.BlockingConnection(parmters)
channel = connection.channel()

# durable = True表示队列持久化
channel.queue_declare(queue = 'hello',durable = True)

messages = ''.join(sys.argv[1:]) or 'Hello World!'
channel.basic_publish(exchange = '', routing_key = 'hello', body = messages,
                     properties = pika.BasicProperties(delivery_mode=2,)) #消息持久化
print 'Send %s' %(messages)

connection.close()