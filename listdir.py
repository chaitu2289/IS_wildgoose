from os import listdir
from os.path import isfile, join

def get_id():
	mypath = "/var/services/homes/kchakka/py-faster-rcnn/VOCdevkit/VOC2007/JPEGImages"
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	return  len(onlyfiles) + 1
