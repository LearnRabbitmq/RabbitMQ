#coding:utf-8
"""
设定交换机的类型（type）为direct。
增加命令行获取参数功能，参数即为路由键。
将队列绑定到交换机上时，设定路由键。

打开两个终端，一个运行代码python receive.py info warning，表示只接收info和warning的消息。
另外一个终端运行send.py，可以观察到接收终端只接收到了info和warning的消息。
如果打开多个终端运行receive.py，并传入不同的路由键参数，可以看到更明显的效果。

当接收端正在运行时，可以使用rabbitmqctl list_bindings来查看绑定情况。
"""
import pika
import sys

credentials = pika.PlainCredentials('admin','admin123')
parmters = pika.ConnectionParameters('192.168.10.154',5672,'my_vhost',credentials)
connection = pika.BlockingConnection(parmters)
# 创建一个通道
channel = connection.channel()  

# 创建一个交换机exchange，并且类型是 direct
channel.exchange_declare(exchange = 'messages', exchange_type = 'direct')

# 从命令行获取路由参数，如果没有，则设置为info
routings = sys.argv[1:]
if not routings:
    routings = ['info']
    
# 生成临时队列，并把临时队列绑定到交换机上，设置路由键
result = channel.queue_declare(exclusive = True)
queue_name = result.method.queue
for routing in routings:
    channel.queue_bind(queue = queue_name, exchange = 'messages', routing_key = routing)

# 定义回调函数
def callback(ch,method,propertis,body):
    print '[x] Recived %s' %(body)
    
channel.basic_consume(callback, queue = queue_name, no_ack = True)
channel.start_consuming()







