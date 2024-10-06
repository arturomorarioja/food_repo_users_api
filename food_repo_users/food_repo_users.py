from flask import Blueprint, request, jsonify
import hashlib
from food_repo_users.database import get_db

def error_message(message='Incorrect parameters'):
    return jsonify({'error': message})

bp = Blueprint('food_repo_users', __name__)

# User creation
@bp.route('/users', methods=['POST'])
def add_user():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')

    if first_name and last_name and email and password:
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        db = get_db()

        sql = '''
        SELECT COUNT(*)
        FROM user
        WHERE cEmail = ?
        '''
        user_count = db.execute(sql, (email,)).fetchone()
        if user_count[0] == 0:
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
            return error_message('A user with this email address already exists'), 400
    else:
        return error_message(), 400
    
# User login validation
@bp.route('/validation', methods=['POST'])
def validate_login():
    email = request.form.get('email')
    password = request.form.get('password')

    if email and password:
        db = get_db()
        sql = '''
            SELECT nUserID, cPassword
            FROM user
            WHERE cEmail = ?
        '''
        user = db.execute(sql, (email,)).fetchone()
        
        if user != None:
            password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if user[1] == password_hash:
                return jsonify({'user_id': user[0]})
            else:
                return error_message('Incorrect password'), 400
        else:
            return error_message('The user does not exist'), 400
    else:
        return error_message(), 400
    
# Management of user favourites
@bp.route('/users/<int:user_id>/favourites', methods=('GET', 'POST', 'DELETE'))
def manage_user_favourites(user_id):
    # Get the list of favourite recipes
    if request.method == 'GET':
        pass
    # Add a new favourite recipe
    elif request.method == 'POST':
        recipe_id = request.form.get('recipe_id')
        db = get_db()
        sql = '''
            SELECT COUNT(*)
            FROM user_favourites
            WHERE nUserID = ?
            AND nRecipeID = ?
        '''
        recipe_count = db.execute(sql, (user_id, recipe_id)).fetchone()
        if recipe_count[0] == 0:
            cursor = db.cursor()
            cursor.execute(
                '''
                    INSERT INTO user_favourites
                        (nUserID, nRecipeID)
                    VALUES
                        (?, ?)
                ''',
                (user_id, recipe_id)
            )
            affected_rows = cursor.rowcount
            cursor.close()
            db.commit()
            if affected_rows > 0:
                return jsonify({'status': 'ok'})
            else:
                return error_message('The recipe could not be added as favourite'), 500
        else:
            return error_message('The user has already favourited this recipe'), 400
    # Delete a favourite recipe
    elif request.method == 'DELETE':
        pass
    else:
        return error_message('Incorrect HTTP method'), 400