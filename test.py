import sys

from flask import Flask, render_template, request, redirect, Response
import random
import json

app = Flask(__name__)


@app.route('/')
def output():
	# serve index template
	return render_template('index.html')


@app.route('/receiver', methods=['GET', 'POST'])
def worker():
	# read json + reply
	data = request.get_json()
	result = ''

	for item in data:
		# loop over every row
		result += str(item['lat']) + '\n'

	return result


if __name__ == '__main__':
	# run!
    app.debug = True
    app.run()
