#!/usr/bin/env python

from os import system
from os.path import join, dirname, abspath
ROOT = dirname(abspath(__file__))
import pika
import sys
sys.path.insert(0, join(ROOT, '..'))
print sys.path
from detect_image import * 
#import Image
import numpy as np
#from pylab import *
#matplotlib.use('Agg')
from image_processing import *
#from caffe_IS.detect_image import *
import json

 
class Receiver:

	def listen(self):
		credentials = pika.PlainCredentials('guest', 'guest')
		connection = pika.BlockingConnection(pika.ConnectionParameters('130.245.168.168', 5672, '/',credentials))
		#connection = pika.BlockingConnection(pika.ConnectionParameters('', 5672, '/',credentials))
		print dir(connection)
		channel = connection.channel()
		channel.queue_declare(queue='argus_queue_')
		channel.basic_qos(prefetch_count=1)
		channel.basic_consume(self.on_request, queue='argus_queue_')
		channel.start_consuming()

	def on_request(self, ch, method, props, body):
		ROOT = dirname(abspath(__file__))
		image = body
		image_store_dir = join(ROOT, '../examples/images')
		caffe_input_file = join(ROOT, '../_temp/det_input.txt')
		
		#copies uploaded image to destination folder
		cmd = join('scp root@130.245.168.168:')
        	cmd += image + ' '
        	cmd += image_store_dir
		system(cmd)

		
		image_file_path = image_store_dir + '/' + image.split('/')[-1] +  ' > ' +  caffe_input_file
		cmd1 = 'echo ' + image_file_path + ' > ' + caffe_input_file
		system(cmd1)
		
		print image
		#I = array(Image.open(image));
		#response = deep_learning("I")
		caffe_output_file = join(ROOT, '../_temp/_output.h5')
		response = detect(caffe_input_file , caffe_output_file)	
		print response
			
		ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id =  props.correlation_id),  body=str(response))
		ch.basic_ack(delivery_tag=method.delivery_tag)

