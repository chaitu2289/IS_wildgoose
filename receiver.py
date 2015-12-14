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
		'''
		This functions listens to the client rabbitmq(130.245.168.168) on port 5672 with queue name _argus_queue 
		'''
		credentials = pika.PlainCredentials('guest', 'guest')
		connection = pika.BlockingConnection(pika.ConnectionParameters('130.245.168.168', 5672, '/',credentials))
		channel = connection.channel()
		channel.queue_declare(queue='_argus_queue')
		channel.basic_qos(prefetch_count=1)
		channel.basic_consume(self.on_request, queue='_argus_queue')
		channel.start_consuming()

	def on_request(self, ch, method, props, body):

		'''
		This function serves three api calls 1) identify_objects 2) save_image 3) learn_features
		'''
		image = json.loads(body)

		#gets the api call
		if "operation" in image:
			operation = image["operation"]
#		if operation == "learn_features":
#			#cmd = "cd /var/services/homes/kchakka/py-faster-rcnn"
#			#system(cmd)
#                        print "Operation is learn_features"
#                        net_name = "VGG16"
#                        weights = "/var/services/homes/kchakka/py-faster-rcnn/data/faster_rcnn_models/VGG16_faster_rcnn_final.caffemodel"
#                        imdb = "voc_2007_train"
#                        train_script = "/var/services/homes/kchakka/py-faster-rcnn/tools/train_faster_rcnn_alt_opt.py"
#                        cmd1 = "python " + train_script + " --net_name=" + net_name + " --weights=" + weights + " --imdb=" + imdb
#                        system(cmd1)
#                        print "Training the network"
#			#cmd = "cd /var/services/homes/kchakka/caffe/argus"
#			#system(cmd)
#			response = "Training done"

		ROOT = dirname(abspath(__file__))
		image_store_dir = join(ROOT, '../examples/images')
                caffe_input_file = join(ROOT, '../_temp/det_input.txt')

		if "image_path" in image:
			#retrive image_name from rabbitmq and generate string(path) to save the image
                	image_name = image["image_path"]
			image_file_path = image_store_dir + '/' + image_name.split('/')[-1]+'.jpg'

                if "image" in image:
			#retrive image and store in temporary location
			im = image["image"]
			[height, width, depth] = im.shape
			img = Image.fromarray(im)
			img.save(image_file_path)

		#dummy response
		#response = deep_learning("I")

		#Using RCNN detector
		#ROOT = dirname(abspath(__file__))
                #image_store_dir = join(ROOT, '../examples/images')
                #caffe_input_file = join(ROOT, '../_temp/det_input.txt')
		#cmd1 = 'echo ' + image_file_path + ' > ' + caffe_input_file
                #system(cmd1)
		#caffe_output_file = join(ROOT, '../_temp/_output.h5')
		#response = detect(caffe_input_file , caffe_output_file)	
	
		#Using Faster RCNN Detector
		if operation == "identify_objects":
			response = detect_objects(image_file_path)
			print response
		elif operation == "save":
			data = image["data"]
			image_id = data["image_id"]
			labels = data["labels"]
			image_shape = [height, width, depth]
			save_path = "/var/services/homes/kchakka/py-faster-rcnn/VOCdevkit/VOC2007/Annotations"
			response = create_xml(image_id, labels, image_shape, save_path)
			fast_rcnn_imagedb = "/var/services/homes/kchakka/py-faster-rcnn/VOCdevkit/VOC2007/JPEGImages/" + response+".jpg"
			img.save(fast_rcnn_imagedb)
			rcnn_image_file_path = "/var/services/homes/kchakka/py-faster-rcnn/VOCdevkit/VOC2007/ImageSets/Main/train.txt"  
			cmd1 = 'echo ' + response + '>>' + rcnn_image_file_path
			system(cmd1)
			print response
		elif operation == "learn_features":
                        #cmd = "cd /var/services/homes/kchakka/py-faster-rcnn"
                        #system(cmd)
                        print "Operation is learn_features"
                        net_name = "VGG16"
                        weights = "/var/services/homes/kchakka/py-faster-rcnn/data/faster_rcnn_models/VGG16_faster_rcnn_final.caffemodel"
                        imdb = "voc_2007_train"
                        train_script = "/var/services/homes/kchakka/py-faster-rcnn/tools/train_faster_rcnn_alt_opt.py"
                        cmd1 = "python " + train_script + " --net_name=" + net_name + " --weights=" + weights + " --imdb=" + imdb
                        system(cmd1)
                        print "Training the network"
                        #cmd = "cd /var/services/homes/kchakka/caffe/argus"
                        #system(cmd)
                        response = "Training done"

			
		ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id =  props.correlation_id),  body=str(response))
		ch.basic_ack(delivery_tag=method.delivery_tag)
