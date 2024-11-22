from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

import db_methods
from jobs_db import User

app = Flask(__name__)

@app.route(rule="/", methods=["GET", "POST"])
def handle_request():
    print('dsgfkaga')
    return jsonify(),200

@app.route('/register', methods=['POST'])
def registerUser():
    login = request.form['login']
    password = request.form['password']
    # firstname = request.form['firstname']
    # lastname = request.form['lastname']
    # middlename = request.form['middlename']
    # birthdate = request.form['birthdate']
    # phone = request.form['phone']
    # email = request.form['email']

    if db_methods.if_exist_user(login):
        return jsonify({'error': 'User exists'}), 401

    hashed_password = generate_password_hash(password)

    db_methods.save_user(
        User(login=login, password=hashed_password))
             # firstName=firstname, lastName=lastname, middleName=middlename,
             # birthDate=birthdate, phone=phone, email=email))

    return jsonify(), 200


@app.route('/login', methods=['POST'])
def loginUser():
    login = request.form['login']
    password = request.form['password']

    if not db_methods.if_exist_user(login):
        return jsonify({'error': 'User not exists'}), 401
    user = db_methods.get_user(login)
    if check_password_hash(user.password, password):
        return jsonify(), 200
    else:
        return jsonify({'error': 'Wrong password'}), 401


if __name__ == '__main__':
    app.run(debug=True)
