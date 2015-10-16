import json

def deep_learning(I):
	points = {"_id":1, "labels":[{"_id":1, "box": [[23, 43], [100,200]], "tag": "chair"}, {"_id":2, "box":[[145, 120],[300, 400]], "tag":"sofa"}]}
	points = json.dumps(points)
	print points
	return points

