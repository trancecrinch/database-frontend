import os, requests, test, uuid, datetime
from flask import Flask, flash, Response, request, send_file, session, jsonify, redirect
from werkzeug.utils import secure_filename

import json_to_topdat, topdat_to_json

# import requests
# import test
# import uuid
# Reference to mongodb: 
# https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb

# TODO: create ALLOWED_EXTENSIONS: set of (conf, top, lammps, pdb, some others, check tacoxdna)
# ALLOWED_EXTENSIONS = set(['conf'])
# mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb

# import pymongo
# C:\Program Files\MongoDB\Server\4.2\bin

from pymongo import MongoClient
client = MongoClient()
# client = MongoClient('localhost', 27017)
db = client.test_database


UPLOAD_FOLDER = os.getcwd() + "/uploads"

app = Flask(__name__)
# app = Flask(__name__, static_url_path="/", static_folder="/")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# @app.route("/dbindex")
# def dbindex():
#     # if session.get("user_id") is not None:
#     return send_file("templates/dbindex.html")

@app.route('/uploadtesting', methods=['GET', 'POST'])
def uploadtesting():

    if request.method == 'POST':
        try:

            f = request.files["file"]
            
        except:
            print ("not available")
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    # if request.method == 'POST':
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        # file = request.files['file']
        # if file.filename == '':
        #     flash('No file selected for uploading')
        #     return redirect(request.url)
        # # if file and allowed_file(file.filename):
        # if file:
        #     filename = file.filename
		# 	# file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     flash('File successfully uploaded')
        #     return redirect('/')
        # else:
        #     flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
        #     return redirect(request.url)
    
    return "successful upload"

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == 'POST':
        
        moleculeType = request.form['moleculeType']
        name = request.form['name']
        tags = request.form['fileFunctionality']

        try:
            fileList = request.files.getlist("file")
        except:
            return "files required!"
    
    # TODO: need to not overwrite files, uuid implementation perhaps? 
    filepaths = []
    for f in fileList:
        path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        filepaths.append(path) 
        f.save(path)
    # TODO: convert all the files into oxDNA format, convert oxDNA format to .json
    for filepath in filepaths:
        post = {"moleculeType" : moleculeType, 
                "name": name,
                "tags": tags,
                "filepath": filepath}
        db.posts.insert_one(post).inserted_id

    return send_file("templates/dbupload.html")

def defaultSearch(parameters):
    default_parameters = {
        'name': None,
        'fid': None,
        'author': None,
        'moleculeType': None,
        'size': None,
        'tags': None,
        'mindateSearch': None,
        'maxdateSearch': None
    }
    for (key, value) in default_parameters.items():
        if value in parameters is None:
            parameters[key] = default_parameters[key]

@app.route("/dbsearch", methods=["GET", "POST"])
def dbsearch():
    parameters = {}
    defaultSearch(parameters)
    try:
        name = request.form['name']
        fid = request.form['id']
        author = request.form['author']
        moleculeType = request.form.getlist('moleculeType')
        size = request.form.getlist('size')
        tags = request.form.getlist('tags')
        minDate = request.form['mindateSearch']
        maxDate = request.form['maxdateSearch']

    except:
        print("notavailable")

    parameters = {
        'name': name,
        'id': fid,
        'author': author,
        'moleculeType': moleculeType,
        'size': size,
        'tags': tags,
        'mindateSearch': minDate,
        'maxdateSearch': maxDate
    }

    print(parameters)
    return "testing"

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

@app.route("/uploadtest", methods=["GET"])
def uploadtest():
    return send_file("templates/upload.html")

@app.route("/")
def index():
	# if session.get("user_id") is not None:
    return send_file("templates/dbindex.html")
	# else:
		# return redirect("/login")

app.run(host="localhost", port=8000)
