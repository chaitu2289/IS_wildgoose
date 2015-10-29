#!/usr/bin/env python
import pika
import Image
import numpy as np
from pylab import *
from image_processing import *
from caffe_IS.detect_image import *
from os import system
from os.path import join, dirname, abspath
 
class Receiver:

	def listen(self):
		connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat_interval=1000))
		channel = connection.channel()
		channel.queue_declare(queue='argus_queue_')
		channel.basic_qos(prefetch_count=1)
		channel.basic_consume(self.on_request, queue='argus_queue_')
		channel.start_consuming()

	def on_request(self, ch, method, props, body):
		image = body
		image_store_dir = 'caffe_IS/examples/images'
		caffe_input_file = 'caffe_IS/_temp/det_input.txt'
		
		#copies uploaded image to destination folder
		cmd = join('cp ')
        	cmd += image + ' '
        	cmd += image_store_dir
		system(cmd)

		#append the path of the
		ROOT = dirname(abspath(__file__))
		
		image_file_path = ROOT + '/' +  image_store_dir + '/' +  image.split('/')[-1] +  ' > ' +  caffe_input_file
		cmd1 = 'echo ' + image_file_path + ' > ' + caffe_input_file
		system(cmd1)
		
		print image
		#I = array(Image.open(image));
		#response = deep_learning("I")
		response = detect('caffe_IS/_temp/det_input.txt' ,'caffe_IS/_temp/_output.h5')	
		print response
			
		ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id =  props.correlation_id),  body=str(response))
		ch.basic_ack(delivery_tag=method.delivery_tag)

