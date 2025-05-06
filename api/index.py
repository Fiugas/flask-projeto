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

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if "username" not in data or "password" not in data:
        return jsonify({"error": "invalid parameters"}), BAD_REQUEST_CODE

    user = db.login(data['username'], data["password"])

    if user is None:
        return jsonify({"error": "Check credentials"}), NOT_FOUND_CODE

    token = jwt.encode(
        {'user_id': user['id'], 'exp': datetime.utcnow() + timedelta(minutes=5)}, app.config['SECRET_KEY'], 'HS256')

    user["token"] = token.decode('UTF-8')
    #user["token"] = token
    return jsonify(user), OK_CODE

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "Authorization" not in request.headers:
            return jsonify({"error": "Token not provided"}), FORBIDDEN_CODE

        token = request.headers['Authorization']
        # Remove Bearer from token
        token = token.split(' ')[1]

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado", "expired": True}), UNAUTHORIZED_CODE
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), FORBIDDEN_CODE

        request.user = db.get_user(data['user_id'])

        return f(*args, **kwargs)

    return decorated

@app.route("/quartos", methods=['POST'])
@auth_required
def insert_reserva():
    data = request.get_json()

    matchs = db.insert_reserva(data, request.user['id'])

    return jsonify(matchs), SUCCESS_CODE

if __name__ == "__main__":
    app.run()