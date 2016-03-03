#coding:utf-8
"""
定义交换机，并且生成一个随机队列，并且把队列绑定到这个交换机上。然后从这个随机队列中获取send端发来的信息
"""
import pika

credentials = pika.PlainCredentials('admin','admin123')
parmeters = pika.ConnectionParameters('192.168.10.154',5672,'my_vhost',credentials)

connection = pika.BlockingConnection(parmeters)

channel = connection.channel()

# 定义交换机
channel.exchange_declare(exchange = 'messages', exchange_type = 'fanout')

# 生成随机队列，并绑定到messages交换机上
# queue_declare的参数exclusive=True表示当接收端退出时，销毁临时产生的队列，这样就不会占用资源
result = channel.queue_declare(exclusive=True)
# 生成随机队列
queue_name = result.method.queue
# 把这个随机队列绑定到交换机上
channel.queue_bind(queue=queue_name,exchange = 'messages', routing_key = '')

def callback(ch,method,properties,body):
    print '[x] Recived %s' %(body)
    
channel.basic_consume(callback, queue = queue_name, no_ack = True)
channel.start_consuming()
