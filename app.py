from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_cors import CORS
from pymongo import MongoClient
app = Flask(__name__)


CORS(app, resources={r"/predict": {"origins": "*"}})

client = MongoClient("mongodb+srv://Akramvd:lF9UjtVXF0iWsxetr2MK@cluster0.7wctpqm.mongodb.net/appdatabase")
db = client.get_database("appdatabase")

@app.route('https://127.0.0.1:8000', methods=['OPTIONS'])
def handle_preflight():
    response = make_response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route('https://127.0.0.1:8000', methods=['POST'])

def predict():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        result = {'prediction': 'niggaooooo '}
        return jsonify(result)
    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)