#coding:utf-8

import pika

# 连接凭证
credentials = pika.PlainCredentials('admin','admin123')
# 连接参数
parmters = pika.ConnectionParameters('192.168.10.154',5672,'my_vhost',credentials)
connection = pika.BlockingConnection(parmters)
channel = connection.channel()

# 声明队列(消息必须放在队列中，才能传递)
# channel.queue_declare(queue='hello')

# 发送消息到上面的队列中
channel.basic_publish(exchange = '', routing_key = 'hello', body = 'Hello World!')
print 'Send Hello World!'
# 关闭连接
connection.close()