# argus

This repository includes code for receiving frontend data(images, bounding boxes) from rabbitmq, creates dataset for the new image in PASCAL VOC format, and initiates training(fine-tuning) on the new and old images in py-faster-rcnn. 

Prerequisites:

Install Rabbitmq

composer.json is in the repo. Execute "composer.phar install"

The above command is used to install "The php-amqplib client library". For any trouble please follow the instructions in "https://www.rabbitmq.com/tutorials/tutorial-one-php.html"

Project Structure:

009963.xml -> Sample xml format to save the image in PASCAL VOC format

detect_objects -> This file should be placed in py-faster-rcnn/tools

create_xml.py -> This file generates xml file for each image(example format 009963.xml)

image_processing.py -> Dummy code that returns bounding boxes

listdir.py -> returns the number of images in PASCAL VOC dataset. This is auxilary file for create_xml.py

receiver.py -> Communicates with rabbitmq and extract all the data sent from GUI.

server.py -> starts rabbitmq server.


