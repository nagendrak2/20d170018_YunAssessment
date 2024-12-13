from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
import json
from datetime import datetime

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'user':
        return 'password'
    return None

def validate_json(f):
    def wrapper(*args, **kwargs):
        data = request.get_json()
        if not data or 'date' not in data or 'amount' not in data:
            return jsonify({'error': 'Invalid JSON data'}), 422
        try:
            datetime.strptime(data['date'], '%d-%m-%Y')
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 422
        return f(*args, **kwargs)
    return wrapper

def validate_query_params(f):
    def wrapper(*args, **kwargs):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date and end_date:
            try:
                datetime.strptime(start_date, '%d-%m-%Y')
                datetime.strptime(end_date, '%d-%m-%Y')
            except ValueError:
                return jsonify({'error': 'Invalid date format in query parameters'}), 422
        return f(*args, **kwargs)
    return wrapper

@app.route('/api/<int:client_id>', methods=['POST'])
@auth.login_required
@validate_json
@validate_query_params
def process_data(client_id):
    data = request.get_json()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Process the data here, e.g., store it in a database, perform calculations, etc.
    # ...

    return jsonify({'message': 'Data processed successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)