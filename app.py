
from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your-secret-key'

users = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    if username in users:
        return jsonify({'error': 'Username already exists'}), 400
    users[username] = password
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    if username not in users or users[username] != password:
        return jsonify({'error': 'Invalid credentials'}), 401
    payload = {'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)}
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token}), 200

@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Missing token'}), 401
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    return jsonify({'message': 'Hello, ' + payload['username']}), 200

if __name__ == '__main__':
    app.run(debug=True)
