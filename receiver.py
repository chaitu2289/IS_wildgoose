#!/usr/bin/env python
import pika
import Image
import numpy as np
from pylab import *
from image_processing import *


 
class Receiver:

	def listen(self):
		connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
		channel = connection.channel()
		channel.queue_declare(queue='argus_queue_')
		channel.basic_qos(prefetch_count=1)
		channel.basic_consume(self.on_request, queue='argus_queue_')
		channel.start_consuming()

	def on_request(self, ch, method, props, body):
		image = body
		#I = array(Image.open(image));
		response = deep_learning("I")
		ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id =  props.correlation_id), body=str(response))
		ch.basic_ack(delivery_tag=method.delivery_tag)

