import os
from flask import Flask, Response, request, send_file, session, jsonify, redirect
import requests
import test

# import Login
# import Job
# import Register
import pymongo

app = Flask(__name__)
# app = Flask(__name__, static_url_path="/", static_folder="/")
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# @app.route("/dbindex")
# def dbindex():
#     # if session.get("user_id") is not None:
#     return send_file("templates/dbindex.html")

@app.route("/upload", methods=["POST"])
def upload():
    json_data = request.get_json()

    parameters = json_data["parameters"]
    files = json_data["files"]
    
    uploadData = {
        "parameters": parameters,
        "files": files
    }
    test.handle(uploadData)
    # print(json_data)
    return "Uploaded!"

@app.route("/dbupload", methods=["GET"])
def dbupload():
    # if session.get("user_id") is not None:
    return send_file("templates/dbupload.html")

@app.route("/dbfilemanager", methods=["GET"])
def dbfilemanager():
    # if session.get("user_id") is not None:
    return send_file("templates/dbfilemanager.html")

@app.route("/upload", methods=["POST"])
def handle_form():
    # if session.get("user_id") is not None:
    # json_data = request.get_json()
    # return json_data
    return 'hello'

@app.route("/")
def index():
	# if session.get("user_id") is not None:
    return send_file("templates/dbindex.html")
	# else:
		# return redirect("/login")

app.run(host="localhost", port=8000)