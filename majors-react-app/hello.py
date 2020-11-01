from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import majorsfair
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

all_dict = majorsfair.organized_dict
majors_dict = []
minors_dict = []
cats_dict = []
dawgs_dict = []
# names_to_zoom_dict

for keys in all_dict.keys():
    if "- Majors" in keys:
        majors_dict = all_dict[keys]
    if "- Minors" in keys:
        minors_dict = all_dict[keys]
    if "- Certificates" in keys:
        cats_dict = all_dict[keys]
    if "- Double Majors" in keys:
        dawgs_dict = all_dict[keys]

# list out all the dictionary stuff

@app.route('/api/', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def api_post():
    if (request.method == 'POST'):
        print(request.get_json())
        #majorsfair.jsonfiles
        # return "hello"
        return majorsfair.jsonfiles
    else:
        return "Hello!"

