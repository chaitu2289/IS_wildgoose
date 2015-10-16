import json

def deep_learning(I):
	points = {"_id":1, "labels":[{"_id":1, "box": [[0, 0], [150,150]], "tag": "chair"}, {"_id":2, "box":[[50, 50],[50, 50]], "tag":"sofa"}]}
	points = json.dumps(points)
	print points
	return points

