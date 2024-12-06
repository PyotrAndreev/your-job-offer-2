from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

import logger
from entities.user import UserModel
from models.hh_token import HH_Token
from models.user import User
from repository.tokens_repository.db_methods import save_hh_token
from repository.vacancies_repository import db_methods
from repository.vacancies_repository.db_methods import update_user

from mappers.mapper import map_vacancy
from repository.vacancies_repository.get_vacancies import get_vacancies

from repository.tokens_repository.get_hh_token import get_hh_token
from use_cases import user_cases
from use_cases.matching import match_vacancies

app = Flask("app")

log = logger.get_logger(__name__)


@app.route('/ping')
def ping():
    # log.error("ping")
    return make_response("OK", 200)


@app.route('/register', methods=['POST'])
def registerUser():
    user = UserModel.from_dict(request.json)

    if db_methods.if_exist_user(user.login):
        return make_response("User exists", 401)
    old_password = user.password
    hashed_password = generate_password_hash(user.password)
    user.password = hashed_password
    user = user_cases.saveUser(user)
    user.password = old_password
    return make_response(user.to_json(), 200)


@app.route('/login', methods=['POST'])
def loginUser():
    user = UserModel.from_dict(request.json)
    if not user_cases.ifExistUser(user.login):
        return make_response("User not exists", 401)
    user_login = user_cases.getUser(user.login)
    print(user)
    if check_password_hash(user_login.password, user.password):
        user_login.password = user.password
        return make_response(user_login.to_json(), 200)
    else:
        return make_response("Wrong password", 401)


@app.route('/get_vacancies', methods=['GET'])
def getVacancies():
    user = UserModel.from_dict(request.json)
    if not user_cases.ifExistUser(user.login):
        return make_response("User not exists", 401)
    user = user_cases.getUser(user.login)
    vac=match_vacancies.get_match_vacancies(user=user)
    return  make_response(vac.to_json())


@app.route('/form', methods=['POST'])
def get_form():
    """
    Handles the POST request for the form submission. Validates the input data,
    updates the user, and returns an appropriate response.

    If the required fields ('login', 'password', 'id') are missing or invalid,
    returns a 400 error with an explanation.

    If an exception occurs during the process, logs the error and returns a 500 error.

    Returns:
        Response: The HTTP response object with status code 200 if successful,
                  or 400/500 if an error occurs.
    """
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
    """
    Handles the POST request for authenticating with hh.ru. It validates the input data and
    saves the provided access and refresh tokens along with the user's login.

    If the required fields ('login', 'access', 'refresh') are missing or invalid,
    returns a 400 error with an explanation.

    If an exception occurs during the process, logs the error and returns a 500 error.

    Returns:
        Response: The HTTP response object with status code 200 if successful,
                  or 400/500 if an error occurs.
    """
    try:
        data = request.json
        if not data or 'access' not in data or 'refresh' not in data or 'login' not in data:
            return make_response(jsonify({"error": "Invalid request. 'login', 'access' and 'refresh' fields are "
                                                   "required."}), 400)

        access_token = data['access']
        refresh_token = data['refresh']
        login = data["login"]
        log.info(f"login={login} \nrefresh_token={refresh_token} \naccess_token={access_token}")
        save_hh_token(HH_Token(login=login, access_token=access_token, refresh_token=refresh_token))
        return make_response("OK", 200)

    except Exception as e:
        log.error(f"Ошибка авторизации на hh.ru: {e}")
        return make_response(jsonify({"error": str(e)}), 500)


@app.route('/test', methods=['POST'])
def test():
    log.info(request.json())
    login = request.json['login']
    log.info(f"login: {login}")
    password = request.json['password']
    log.info(f"password: {password}")
    hh_token = get_hh_token(login)
    log.info(hh_token)
    return make_response(hh_token.to_json(), 200)


@app.route('/some', methods=['GET'])
def some():
    user=user_cases.getUser(login="admin")
    vacs=match_vacancies.get_match_vacancies(user)
    print(vacs)
    return make_response(vacs, 200)