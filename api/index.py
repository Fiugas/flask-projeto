import os
from datetime import datetime, timedelta
from functools import wraps

import jwt
import psycopg2
from flask import Flask, jsonify, request

import db

# Flask config
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

# Página inicial
@app.route('/', methods = ["GET"])
def home():
    return "Welcome to API!"

# Login
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

# Registo
@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()

    if "username" not in data or "password" not in data:
        return jsonify({"error": "invalid parameters"}), BAD_REQUEST_CODE

    if (db.user_exists(data)):
        return jsonify({"error": "user already exists"}), BAD_REQUEST_CODE

    user = db.add_user(data)

    return jsonify(user), SUCCESS_CODE

# Tokens JWT
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

# Reserva quarto
@app.route("/reservas", methods=['POST'])
@auth_required
def insert_reserva():
    matchs = db.insert_reserva()
    return jsonify(matchs), SUCCESS_CODE

# Consulta reservas
@app.route("/reservas/<int:id_quarto>/<data>", methods=['GET'])
@auth_required
def get_disponibilidade(id_quarto, data):
    match = db.get_disponibilidade(id_quarto, data)
    if match is None:
        return jsonify({"error": "No content"}), NO_CONTENT_CODE
    return jsonify(match), OK_CODE

# Pagamento da reserva
@app.route("/pagamentos", methods=['POST'])
@auth_required
def pagamento():
    matchs = db.pagamento()
    return jsonify(matchs), SUCCESS_CODE

# Cancela reserva
@app.route("/reservas/{id}/cancelar", methods=['PUT'])
@auth_required
def cancel():
    matchs = db.cancel()
    return jsonify(matchs), SUCCESS_CODE

# Upload de imagem
@app.route("/upload-imagem", methods=['POST'])
@auth_required
def upload():
    matchs = db.upload()
    return jsonify(matchs), SUCCESS_CODE

# Ver imagem do quarto
@app.route("/quartos/{id}/imagem", methods=['POST'])
@auth_required
def ver_imagem():
    matchs = db.ver_imagem()
    return jsonify(matchs), SUCCESS_CODE

if __name__ == "__main__":
    app.run()