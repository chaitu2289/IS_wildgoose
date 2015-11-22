import xml.etree.cElementTree as ET
from listdir import *


def create_file(xmin, xmax, ymin, ymax, tag, image_shape):
	root = ET.Element("annotation")
	ET.SubElement(root, "folder").text = "VOC2007"
	ET.SubElement(root, "filename").text = str(get_id())
	
	source = ET.SubElement(root, "source")
	ET.SubElement(source, "database").text = "The VOC2007 Database"
	ET.SubElement(source, "annotation").text = "PASCAL VOC2007"
	ET.SubElement(source, "image").text = "chaitu"
	
	size = ET.SubElement(root, "size")
	ET.SubElement(size, "width").text = str(image_shape[1])
	ET.SubElement(size, "height").text = str(image_shape[0])
	ET.SubElement(size, "depth").text = str(image_shape[2])
	
	ET.SubElement(root, "segmented").text = "0"
	
	_object = ET.SubElement(root, "object")
	ET.SubElement(_object, "name").text = tag
	ET.SubElement(_object, "pose").text = "Frontal"
	ET.SubElement(_object, "truncated").text = "1"
	ET.SubElement(_object, "difficult").text = "0"
	
	bbox = ET.SubElement(_object, "bbox")
	ET.SubElement(bbox, "xmin").text = str(xmin)
	ET.SubElement(bbox, "xmax").text = str(xmax)
	ET.SubElement(bbox, "ymin").text = str(ymin)
	ET.SubElement(bbox, "ymax").text = str(ymax)
	_id = str(get_id())
	file_name_length = len(str(get_id()))
	num_zeros = 6 - file_name_length
	zeros = ""
	for i in range(num_zeros):
		zeros = zeros + "0"
	file_name = zeros + _id
	print file_name
	tree = ET.ElementTree(root)
	tree.write(file_name + ".xml")

def create_xml(image_id, labels, image_shape):
	for i in range(len(labels)):
		box = labels[i]["box"]
		x_min = box[0][0]
		y_min = box[0][1]
		width = int(box[1][0])
		height = int(box[1][1])
		x_max = x_min + width
		y_max = y_min + height
		tag = labels[i]["label"]
		print tag
		create_file(x_min, y_min, x_max, y_max, tag, image_shape)
		#print [(x_min, y_min), (x_max, y_max) ]
		#print "labels", labels[0]
