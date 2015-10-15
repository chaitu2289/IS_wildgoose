import json

def deep_learning(I):
	points = {"_id":1, "labels":[{"_id":1, "box": [[23, 43], [100,200]], "label": "chair"}, {"_id":2, "box":[[145, 120],[300, 400]], "label":"sofa"}]}
	#json_points = json.dumps(points)
	print points
	return points

