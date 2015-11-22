#!/usr/bin/env python

from os import system
from os.path import join, dirname, abspath
ROOT = dirname(abspath(__file__))
import pika
import sys
#sys.path.insert(0, join(ROOT, '..'))
#from detect_image import *
sys.path.insert(0,join(ROOT, '../../py-faster-rcnn/tools'))
from chaitu_detect_objects import *
from create_xml import *
#import Image
import numpy as np
from PIL import Image
#from pylab import *
#matplotlib.use('Agg')
from image_processing import *
#from caffe_IS.detect_image import *
from jaweson import json
 
class Receiver:

	def listen(self):
		credentials = pika.PlainCredentials('guest', 'guest')
		connection = pika.BlockingConnection(pika.ConnectionParameters('130.245.168.168', 5672, '/',credentials))
		#connection = pika.BlockingConnection(pika.ConnectionParameters('', 5672, '/',credentials))
		channel = connection.channel()
		channel.queue_declare(queue='_argus_queue')
		channel.basic_qos(prefetch_count=1)
		channel.basic_consume(self.on_request, queue='_argus_queue')
		channel.start_consuming()

	def on_request(self, ch, method, props, body):
		image = json.loads(body)
		if "operation" in image:
			operation = image["operation"]
                image_name = image["image_path"]

                im = image["image"]
		[height, width, depth] = im.shape

		img = Image.fromarray(im)
		#[height, width, depth] = img.shape
		#print height, width, depth

		ROOT = dirname(abspath(__file__))
		#image = body
		image_store_dir = join(ROOT, '../examples/images')
		caffe_input_file = join(ROOT, '../_temp/det_input.txt')
		
		#copies uploaded image to destination folder
		#cmd = join('scp root@130.245.168.168:')
        	#cmd += image + ' '
        	#cmd += image_store_dir
		#system(cmd)

		image_file_path = image_store_dir + '/' + image_name.split('/')[-1]+'.jpg'
		img.save(image_file_path)
		cmd1 = 'echo ' + image_file_path + ' > ' + caffe_input_file
		system(cmd1)
		
		#print image
		#dummy response
		#response = deep_learning("I")

		#Using RCNN detector
		#caffe_output_file = join(ROOT, '../_temp/_output.h5')
		#response = detect(caffe_input_file , caffe_output_file)	
	
		#Using Faster RCNN Detector
		if operation == "identify_objects":
			response = detect_objects(image_file_path)
			print response
		elif operation == "learn_features":
			data = image["data"]
			image_id = data["image_id"]
			labels = data["labels"]
			image_shape = [height, width, depth]
			response = create_xml(image_id, labels, image_shape)
			print response
			
		ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id =  props.correlation_id),  body=str(response))
		ch.basic_ack(delivery_tag=method.delivery_tag)


