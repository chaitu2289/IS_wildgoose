#!/usr/bin/env python
import pika
import Image
import numpy as np
from pylab import *


 

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='argus_queue_')


def on_request(ch, method, props, body):
	image = body
	print body
	I = array(Image.open(image));
	print I[0][0]
	response = I[0][0]
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id =  props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='argus_queue_')


channel.start_consuming()
