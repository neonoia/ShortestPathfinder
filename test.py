import sys

from flask import Flask, render_template, request, redirect, Response, jsonify
import random
import json
from math import sin, cos, sqrt, atan2, radians

app = Flask(__name__)

@app.route('/')
def output():
	# serve index template
	return render_template('index.html')

@app.route('/receiver', methods=['POST'])
def worker():
	# read json + reply
	data = request.get_json(force = True)
	coord = []

	for i in range(1,len(data) + 1):
		cont = []
		cont.append(data[str(i)]['lat'])
		cont.append(data[str(i)]['lng'])
		coord.append(cont)
	
	print(coord)

	return jsonify(data)

# function to calculate distance between 2 points
def dist(p1, p2):
	# approximate radius of earth in km
	R = 6373.0
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c
	return distance

if __name__ == '__main__':
	# run!
    app.debug = True
    app.run()
