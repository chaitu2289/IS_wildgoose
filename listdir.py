from os import listdir
from os.path import isfile, join

def get_id():
        """
	This function returns the rank of the newly added xml file by counting the number of existing .xml files and adding 1
        """
	mypath = "/var/services/homes/kchakka/py-faster-rcnn/VOCdevkit/VOC2007/JPEGImages"
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	return  len(onlyfiles) + 1
