import json
import os
import uuid

from flask import Flask, request, jsonify, send_file, render_template

app = Flask(__name__)
chunk_size = 4096


@app.route('/')
def hello():
	return render_template('index.html')


@app.after_request
def add_header(response):
	response.headers['Access-Control-Allow-Origin'] = "*"
	response.headers['Access-Control-Allow-Methods'] = "*"
	response.headers['Access-Control-Allow-Headers'] = "*"
	return response


@app.route('/upload/<username>', methods=['GET', 'PUT'])
def hello_world(username):
	if request.headers.get("Token", "test") == os.getenv('INVITE'):
		filename = str(uuid.uuid1())
		oof = open(filename + ".data", "wb")
		ooff = open(filename + ".info", "w")
		while True:
			chunk = request.stream.read(chunk_size)
			oof.write(chunk)
			if len(chunk) == 0:
				oof.close()
				break
		ooff.write(username)
		ooff.close()
		return jsonify({"name": username, "uuid": filename})
	else:
		return "error", 500


@app.route('/pub/<uuid>')
def downloadFile(uuid):
	ooff = open(uuid + ".info", "r")
	fn = ooff.read()
	ooff.close()
	return send_file(uuid + ".data", download_name=fn, as_attachment=True)


if __name__ == '__main__':
	app.run(host="0.0.0.0")
