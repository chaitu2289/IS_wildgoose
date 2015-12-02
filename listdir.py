from os import listdir
from os.path import isfile, join

def get_id():
	mypath = "/var/services/homes/kchakka/py-faster-rcnn/VOCdevkit/VOC2007/JPEGImages"
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	
	#file_number = str(len(onlyfiles))
	#file_name_length = len(file_number)
	#max_file_name_length = 6
	#zeros = ""
	#for i in range(max_file_name_length - file_name_length):
	#	zeros = zeros + "0"
	#file_name = "zeros" + file_number + ".jpg"	
	return  len(onlyfiles) + 1
