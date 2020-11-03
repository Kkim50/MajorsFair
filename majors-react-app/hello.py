from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import majorsfair
import logging
#from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
# UPLOAD_FOLDER = "./"
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/api/upload/', methods=['GET', 'POST'])
# @cross_origin(supports_credentials=True)
# def upload():
#     if(request.method == 'POST'):
#         f = request.form
#         for key in f.keys():
#             for value in f.getlist(key):
#                 print (key,":",value)
#         return "Error"

@app.route('/api/', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def api_post():
    if (request.method == 'POST'):
        return majorsfair.jsonfiles
    else:
        return "Hello World!"
