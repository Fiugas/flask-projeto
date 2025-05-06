import os
from datetime import datetime, timedelta
from functools import wraps

import jwt
import psycopg2
from flask import Flask, jsonify, request

import db

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mysecretkey')

NOT_FOUND_CODE = 401
OK_CODE = 200
SUCCESS_CODE = 201
NO_CONTENT_CODE = 204
BAD_REQUEST_CODE = 400
UNAUTHORIZED_CODE = 401
FORBIDDEN_CODE = 403
NOT_FOUND = 404
SERVER_ERROR = 500

@app.route('/', methods = ["GET"])
def home():
    return "Welcome to API!"

@app.route("/reserva", methods=['POST'])
def insert_reserva():
    #data = request.get_json()

    matchs = db.insert_reserva()

    return jsonify(matchs), SUCCESS_CODE

@app.route('/disponibilidade/<int:id_quarto>/<data>', methods=['GET'])
def get_disponibilidade(id_quarto, data):
    match = db.get_disponibilidade(id_quarto, data)
    if match is None:
        return jsonify({"error": "No content"}), NO_CONTENT_CODE
    return jsonify(match), OK_CODE

if __name__ == "__main__":
    app.run()