#coding:utf-8

import pika

# 连接rabbitmq服务器参数
credentials = pika.PlainCredentials('admin','admin123')
parmters = pika.ConnectionParameters('192.168.10.154',5672,'my_vhost',credentials)
# 连接rabbitmq 服务器
connection = pika.BlockingConnection(parmters)
channel = connection.channel()

# 声明队列
channel.queue_declare(queue = 'hello')

# 定义回调函数
def callback(ch, method, properties,body):
    print 'Recived %s' %(body)

# 告诉rabbitmq使用callback来接收信息   
channel.basic_consume(callback, queue = 'hello', no_ack = True)

# 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理。按ctrl+c退出
channel.start_consuming()