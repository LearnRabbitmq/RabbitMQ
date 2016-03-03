#coding:utf-8

"""
交换机的类型要设定为topic就可以了。从命令行接收参数的功能稍微调整了一下，就是没有参数时报错退出
"""
import pika
import sys


credentials = pika.PlainCredentials('admin','admin123')
parmters = pika.ConnectionParameters('192.168.10.154',5672,'my_vhost',credentials)
connection = pika.BlockingConnection(parmters)
channel = connection.channel()

# 定义交换机exchange，类型为topic
channel.exchange_declare(exchange = 'messages',
                         exchange_type = 'topic')

# 定义随机队列，并把这个队列绑定到exchange上去
result = channel.queue_declare(exclusive = True)
queue_name = result.method.queue
routings = sys.argv[1:]
if not routings:
    print >> sys.stderr, "Usage: %s [routing_key]" %(sys.argv[0])
    exit()
for routing in routings:
    channel.queue_bind(queue = queue_name, exchange = 'messages', 
                   routing_key = routing)
    
def callback(ch,method,properties,body):
    print "[x] Recived %s" %(body)

channel.basic_consume(callback, queue = queue_name, no_ack = True)
channel.start_consuming()

"""
1、发送信息时，如果不设置路由键，那么路由键设置为”*”的接收端是否能接收到消息？

发送信息时，如果不设置路由键，默认是表示广播出去，理论上所有接收端都可以收到消息，但是笔者试了下，路由键设置为"*"的接收端收不到任何消息。

只有发送消息时，设置路由键为一个词，路由键设置为"*"的接收端才能收到消息。在这里，每个词使用"."符号分开的。
2、发送消息时，如果路由键设置为”..”，那么路由键设置为”#.*”的接收端是否能接收到消息？如果发送消息时，路由键设置为一个词呢？

两种情况，笔者都测试过了，可以的。
3、”a.*.#” 和”a.#”的区别

"a.#"只要字符串开头的一个词是a就可以了，比如a、a.haha、a.haha.haha。而这样的词是不行的，如abs、abc、abc.haha。

"a.*.#"必须要满足a.*的字符串才可以，比如a.、a.haha、a.haha.haha。而这样的词是不行的，如a。
"""


