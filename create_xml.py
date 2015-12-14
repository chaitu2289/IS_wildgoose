import xml.etree.cElementTree as ET
from listdir import *

"""
This file creates an xml file in PASCAL VOC format describing the image
Example format of the xml file : Refer "009963.xml" in this repo
"""

def create_file(xmin, ymin, xmax, ymax, tag, image_shape, save_path):
	root = ET.Element("annotation")
	ET.SubElement(root, "folder").text = "VOC2007"
	file_name = str(get_id())
	file_name_length = len(str(get_id()))
        num_zeros = 6 - file_name_length
        zeros = ""
        for i in range(num_zeros):
                zeros = zeros + "0"
        file_name = zeros + _id
	ET.SubElement(root, "filename").text = file_name + ".jpg"
	
	source = ET.SubElement(root, "source")
	ET.SubElement(source, "database").text = "The VOC2007 Database"
	ET.SubElement(source, "annotation").text = "PASCAL VOC2007"
	ET.SubElement(source, "image").text = "chaitu"
	
	size = ET.SubElement(root, "size")
	ET.SubElement(size, "width").text = str(image_shape[1])
	ET.SubElement(size, "height").text = str(image_shape[0])
	ET.SubElement(size, "depth").text = str(image_shape[2])
	
	ET.SubElement(root, "segmented").text = "0"

	for i in range(len(xmin)):
	
		_object = ET.SubElement(root, "object")
		ET.SubElement(_object, "name").text = tag[i]
		ET.SubElement(_object, "pose").text = "Frontal"
		ET.SubElement(_object, "truncated").text = "1"
		ET.SubElement(_object, "difficult").text = "0"
		
		bbox = ET.SubElement(_object, "bndbox")
		ET.SubElement(bbox, "xmin").text = str(xmin[i])
		ET.SubElement(bbox, "xmax").text = str(xmax[i])
		ET.SubElement(bbox, "ymin").text = str(ymin[i])
		ET.SubElement(bbox, "ymax").text = str(ymax[i])
	"""
	Generate file name for .xml format. File name contains 6 digits denotes the rank of the file 
        in the training set. Eg: "009963.xml" is the 9963th file in the training set
	"""
	_id = str(get_id())
	file_name_length = len(str(get_id()))
	num_zeros = 6 - file_name_length
	zeros = ""
	for i in range(num_zeros):
		zeros = zeros + "0"
	file_name = zeros + _id
	print file_name
	tree = ET.ElementTree(root)
	tree.write(save_path +"/" +  file_name + ".xml")
	return file_name

def create_xml(image_id, labels, image_shape, save_path):
	'''
Arguments

image_id - Currently not using image_id
labels   - All user annotated labels which are in the format
[
  {
    _id : "1"	
    box : [[x_min, y_min], [width, height]]
    label : chair
  }
]
image_shape - dimensions of the image size
save_path - store the xml in the training data set in py-faster-rcnn
	'''
	x_min = []
	y_min = []
	x_max = []
	y_max = []
	tag = []
	for i in range(len(labels)):
		box = labels[i]["box"]
		x_min.append(box[0][0])
		y_min.append(box[0][1])
		width = int(box[1][0])
		height = int(box[1][1])
		x_max.append(x_min[i] + width)
		y_max.append(y_min[i] + height)
		tag.append(labels[i]["label"])
		print tag
	file_name = create_file(x_min, y_min, x_max, y_max, tag, image_shape, save_path)
	return file_name
