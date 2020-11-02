from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import majorsfair
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/api/', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def api_post():
    if (request.method == 'POST'):
        print(request.get_json())
        return majorsfair.jsonfiles
    else:
        return "Hello!"

