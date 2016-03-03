#coding:utf-8

"""
路由键的工作原理：每个接收端的消息队列在绑定交换机的时候，可以设定相应的路由键。
发送端通过交换机发送信息时，可以指明路由键 ，
交换机会根据路由键把消息发送到相应的消息队列，这样接收端就能接收到消息了。

设定交换机的类型（type）为direct。上一篇是设置为fanout，表示广播的意思，会将消息发送到所有接收端，
这里设置为direct表示要根据设定的路由键来发送消息。
发送信息时设置发送的路由键。
"""
import pika

credentials = pika.PlainCredentials('admin','admin123')
parmters = pika.ConnectionParameters('192.168.10.154',5672,'my_vhost',credentials)
connection = pika.BlockingConnection(parmters)
# 创建一个通道
channel = connection.channel()  

# 创建一个交换机exchange，并且类型是 direct
channel.exchange_declare(exchange = 'messages', exchange_type = 'direct')

# 定义三个路由键
routings = ['info','warning','error']

# 将消息依次发送到交换机上
for routing in routings:
    messages = '%s messages' %(routing)
    channel.basic_publish(exchange = 'messages', routing_key = routing, body = messages)
    print messages
    
connection.close()







