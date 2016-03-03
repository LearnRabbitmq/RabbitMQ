#coding:utf-8
"""
主要是定义交换机，类型是fanout(广播)，并且把消息发送给交换机
"""
import pika

credentials = pika.PlainCredentials('admin','admin123')
parmters = pika.ConnectionParameters('192.168.10.154',5672,'my_vhost',credentials)

connection = pika.BlockingConnection(parmters)

channel = connection.channel()

# 定义交换机exchange,类型是fanou的是广播到bangding到这个交换机的所有队列
channel.exchange_declare(exchange = 'messages', exchange_type = 'fanout')
    
# 将消息发送到交换机
# basic_publish方法的参数exchange被设定为相应交换机，因为是要广播出去，发送到所有队列，所以routing_key就不需要设定了
channel.basic_publish(exchange = 'messages', routing_key = '', body = 'Hello World!')

print "[x] Send 'Hello World!' "

connection.close()