#coding:utf-8

import pika

credentials = pika.PlainCredentials('admin','admin123')
parmters = pika.ConnectionParameters('192.168.10.154',5672,'my_vhost',credentials)
connection = pika.BlockingConnection(parmters)
channel = connection.channel()

# 定义接受消息的队列
channel.queue_declare(queue = 'compute_queue')
print '[*] Waiting for n'
# 将n的值加1
def increase(n):
    return n + 1

# 定义接受消息的处理方法
def request(ch,method,properties,body):
    response = increase(int(body))
    
    # 将计算的结果返回控制中心
    ch.basic_publish(exchange = '', 
                          routing_key = properties.reply_to, 
                          body = str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count = 1)
channel.basic_consume(request, queue = 'compute_queue', no_ack = True)
channel.start_consuming()
