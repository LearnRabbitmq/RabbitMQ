#coding:utf-8

"""
处理方法描述：发送端在发送信息前，产生一个接收消息的临时队列，该队列用来接收返回的结果。
其实在这里接收端、发送端的概念已经比较模糊了，因为发送端也同样要接收消息，接收端同样也要发送消息，所以这里笔者使用另外的示例来演示这一过程。

示例内容：假设有一个控制中心和一个计算节点，控制中心会将一个自然数N发送给计算节点，
计算节点将N值加1后，返回给控制中心。这里用center.py模拟控制中心，compute.py模拟计算节点。
"""
#coding:utf-8

import pika

class Center(object):
    def __init__(self):
        # 连接rabbitmq服务器
        self.credentials = pika.PlainCredentials('admin','admin123')
        self.parmters = pika.ConnectionParameters('192.168.10.154',5672,
                                                  'my_vhost',self.credentials)
        self.connection = pika.BlockingConnection(self.parmters)
        self.channel = self.connection.channel()
    
        # 定义随机返回队列
        self.result = self.channel.queue_declare(exclusive = True)
        self.callback_queue = self.result.method.queue
        self.channel.basic_consume(self.on_response, queue = self.callback_queue, no_ack = True)
        
    # 定义返回回调函数
    def on_response(self,ch,method,properties,body):
        self.response = body
        
    # 发送消息到计算节点,并使用properties指定返回的队列的名称
    def request(self,n):
        self.response = None
        self.channel.publish(exchange = '', routing_key = 'compute_queue', 
                             body = str(n), 
                             properties = pika.BasicProperties(reply_to= self.callback_queue))
        
        # 接受返回的数据
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)

center = Center() 

print "Request increase(30)"
response = center.request(30)
print "Got %s" %(response) 
        
        
        
