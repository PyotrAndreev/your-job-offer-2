
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

import logger
from entities.user import UserModel
from models.hh_token import HH_Token
from models.user import User
from repository.tokens_repository.db_methods import save_hh_token
from repository.vacancies_repository import db_methods
from repository.vacancies_repository.db_methods import update_user

app = Flask("app")

log = logger.get_logger(__name__)


@app.route('/ping')
def ping():
    return make_response("OK", 200)


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
    try:
        data = request.json
        if not data or 'login' not in data or 'password' not in data or 'id' not in data:
            return make_response(jsonify({"error": "Invalid request. 'login', 'password', 'id' fields are "
                                                   "required."}), 400)

        user = UserModel.from_json(data)
        update_user(user)
        return make_response("OK", 200)
    except Exception as e:
        log.error(f"Ошибка сохранения данных из формы: {e}")
        return make_response(jsonify({"error": str(e)}), 500)


@app.route('/hh_auth', methods=['POST'])
def hh_auth():
    try:
        data = request.json
        if not data or 'access' not in data or 'refresh' not in data or 'login' not in data:
            return make_response(jsonify({"error": "Invalid request. 'login', 'access' and 'refresh' fields are "
                                                   "required."}), 400)

        access_token = data['access']
        refresh_token = data['refresh']
        login = data["login"]
        save_hh_token(HH_Token(login=login, access_token=access_token, refresh_token=refresh_token))
        return make_response("OK", 200)

    except Exception as e:
        log.error(f"Ошибка авторизации на hh.ru: {e}")
        return make_response(jsonify({"error": str(e)}), 500)


