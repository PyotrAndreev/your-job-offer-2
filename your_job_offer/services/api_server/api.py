from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from services.vacancies_repository import db_methods

app = Flask("app")


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
        return make_response("User not exists", 401)

    hashed_password = generate_password_hash(password)
    db_methods.save_user(User(login=login, password=hashed_password))
    # firstName=firstname, lastName=lastname, middleName=middlename,
    # birthDate=birthdate, phone=phone, email=email))

    return make_response("OK", 200)


@app.route('/login', methods=['POST'])
def loginUser():
    login = request.form['login']
    password = request.form['password']
    user1 = db_methods.if_exist_user(login)
    print(user1)
    if not user1:
        return make_response("User not exists", 401)
    user = db_methods.get_user(login)
    print(user)
    if check_password_hash(user.password, password):
        return make_response("OK", 200)
    else:
        return make_response("Wrong password", 401)

@app.route('/form', methods=['POST'])
def get_form():
    if not request.json or not 'user' in request.json:
        abort(400)

    return make_response("OK", 200)


@app.route('/hh_auth', methods=['POST'])
def hh_auth():
    if not request.json or not 'user' in request.json:
        abort(400)

    return make_response("OK", 200)


@app.route('/cv', methods=['POST'])
def hh_auth():
    if not request.json or not 'user' in request.json:
        abort(400)

    return make_response("OK", 200)


@app.route('/cv', methods=['GET'])
def hh_auth():
    if not request.json or not 'user' in request.json:
        abort(400)

    return make_response("OK", 200)
