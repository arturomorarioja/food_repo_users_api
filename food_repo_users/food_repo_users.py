from flask import Blueprint, request, jsonify
import hashlib
from food_repo_users.database import get_db

def error_message():
    return jsonify({'error': 'Incorrect parameters'})

bp = Blueprint('food_repo_users', __name__)

@bp.route('/users', methods=['POST'])
def add_user():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    if first_name and last_name and email and password:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            '''
                INSERT INTO user
                    (cFirstName, cLastName, cEmail, cPassword)
                VALUES 
                    (?, ?, ?, ?)
            ''',
            (first_name, last_name, email, password_hash)
        )
        user_id = cursor.lastrowid
        cursor.close()
        db.commit()
        return jsonify({'user_id': user_id}), 201
    else:
        return error_message(), 400