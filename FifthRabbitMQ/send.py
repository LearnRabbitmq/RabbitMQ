#coding:utf-8
"""
路由键模糊匹配，就是可以使用正则表达式，和常用的正则表示式不同，
这里的话“#”表示所有、全部的意思；“*”只匹配到一个词。
"""
import pika

credentials = pika.PlainCredentials('admin','admin123')
parmters = pika.ConnectionParameters('192.168.10.154',5672,'my_vhost',credentials)
connection = pika.BlockingConnection(parmters)
channel = connection.channel()

# 定义一个交换机exchange，类型是topic
channel.exchange_declare(exchange = 'messages', exchange_type = 'topic')

#定义routing key
routings = ['happy.life','happy.work','bad.life','bad.work']

#把消息发送到交换机
for routing in routings:
    message = "%s message" %(routing)
    channel.basic_publish(exchange = 'messages', 
                          routing_key = routing, body = message)
    print message
    
connection.close()
    