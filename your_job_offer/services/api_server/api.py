import json
import os
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import Enum
import your_job_offer.logger as logger
from your_job_offer.entities.jobs import VacancyModel
from your_job_offer.entities.user import UserModel
from your_job_offer.models.hh_token import HH_Token
from your_job_offer.repository.tokens_repository.db_methods import (
    save_hh_token,
)
from your_job_offer.repository.vacancies_repository import db_methods
from your_job_offer.repository.vacancies_repository.db_methods import (
    update_user,
)

from your_job_offer.repository.tokens_repository.get_hh_token import (
    get_hh_token,
)
from your_job_offer.services.hh_api.apply_to_vacancy import apply_to_vacancy
from your_job_offer.use_cases import user_cases
from your_job_offer.use_cases.matching import match_vacancies
from your_job_offer.use_cases.user_cases import getUser, saveUser
from your_job_offer.services.cv_parser.methods import parse
from your_job_offer.repository.vacancies_repository.get_professional_roles import get_professional_roles
from your_job_offer.services.hh_api.create_new_resume import create_new_resume
from your_job_offer.services.hh_api.publish_resume import publish_resume
from your_job_offer.services.hh_api.update_resume import update_resume
from your_job_offer.repository.vacancies_repository.db_methods import update_statuses
from your_job_offer.entities.enums import StatusEnum
from datetime import date, datetime
import enum


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, enum.Enum):
        return obj.value
    raise TypeError("Type %s not serializable" % type(obj))


app = Flask("app")

log = logger.get_logger(__name__)


@app.route("/ping")
def ping():
    get_professional_roles()
    return make_response("OK", 200)


@app.route("/register", methods=["POST"])
def registerUser():
    user = UserModel.from_dict(request.json)

    if db_methods.if_exist_user(user.login):
        return make_response("User exists", 401)
    old_password = user.password
    hashed_password = generate_password_hash(user.password)
    user.password = hashed_password
    user = user_cases.saveUser(user)
    user.password = old_password
    return make_response(user.to_json(default=json_serial), 200)


@app.route("/login", methods=["POST"])
def loginUser():
    user = UserModel.from_dict(request.json)
    if not user_cases.ifExistUser(user.login):
        return make_response("User not exists", 401)
    user_login = user_cases.getUser(user.login)
    print(user)
    if check_password_hash(user_login.password, user.password):
        user_login.password = user.password
        return make_response(user_login.to_json(default=json_serial), 200)
    else:
        return make_response("Wrong password", 401)


@app.route("/get_vacancies", methods=["POST"])
def getVacancies():
    user = UserModel.from_dict(request.json)
    if not user_cases.ifExistUser(user.login):
        return make_response("User not exists", 401)
    vac: list[VacancyModel] = match_vacancies.get_match_vacancies(user=user)
    return make_response('{"vacancies":'
                         + json.dumps([json.loads(v.to_json(default=json_serial)) for v in vac]) + "}",
                         200, )


@app.route("/get_status", methods=["POST"])
def getStatuses():
    user = UserModel.from_dict(request.json)
    if not user_cases.ifExistUser(user.login):
        return make_response("User not exists", 401)
    user = user_cases.getUser(user.login)
    return make_response(
        '{"vacancies":' + json.dumps([json.loads(v.to_json(default=json_serial)) for v in user.vacancy])
        + "}", 200,
    )


@app.route("/form", methods=["POST"])
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
        if not data or "login" not in data or "password" not in data:
            return make_response(
                jsonify(
                    {
                        "error": "Invalid request. 'login', 'password' fields are "
                                 "required."
                    }
                ),
                400,
            )

        user = UserModel.from_json(request.data)
        log.info(f"User: {user}")
        hh_token = get_hh_token(user.login)
        resume_id = create_new_resume(user=user, access_token=hh_token.access_token)
        if resume_id == None:
            return make_response(jsonify({"error": "bad form"}), 404)
        is_published = publish_resume(resume_id=resume_id, access_token=hh_token.access_token)
        if not is_published:
            return make_response(jsonify({"error": "bad form"}), 404)
        user.hh_resume_id = resume_id
        user_cases.updateUser(user)
        return make_response("OK", 200)
    except Exception as e:
        log.error(f"Ошибка сохранения данных из формы: {e}")
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/hh_auth", methods=["POST"])
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
        if (
                not data
                or "access" not in data
                or "refresh" not in data
                or "login" not in data
        ):
            return make_response(
                jsonify(
                    {
                        "error": "Invalid request. 'login', 'access' and 'refresh' fields are "
                                 "required."
                    }
                ),
                400,
            )

        access_token = data["access"]
        refresh_token = data["refresh"]
        login = data["login"]
        log.info(
            f"login={login} \nrefresh_token={refresh_token} \naccess_token={access_token}"
        )
        save_hh_token(
            HH_Token(
                login=login,
                access_token=access_token,
                refresh_token=refresh_token,
            )
        )
        return make_response("OK", 200)

    except Exception as e:
        log.error(f"Ошибка авторизации на hh.ru: {e}")
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/apply", methods=["POST"])
def apply():
    try:
        data = request.json
        if (
                not data
                or "user" not in data
                or "vacancy" not in data
        ):
            return make_response(
                jsonify(
                    {
                        "error": "Invalid request. 'user', 'vacancy' fields are "
                                 "required."
                    }
                ),
                400,
            )
        user_data = json.dumps(data.get("user"))
        user = UserModel.from_json(user_data)

        vacancy = json.dumps(data.get("vacancy"))
        vacancy = VacancyModel.from_json(vacancy)

        hh_token = get_hh_token(user.login)
        vacancy_id = vacancy.id_vacancy_from_source
        user_bd = getUser(user.login)
        nid = apply_to_vacancy(
            vacancy_id=vacancy_id,
            access_token=hh_token.access_token,
            resume_id=user_bd.hh_resume_id,
        )
        if nid == None:
            return make_response(jsonify({"error": "can not apply"}), 404)
        # user.vacancy = user_bd.vacancy
        user.vacancy.append(vacancy)
        update_statuses(vacancy.id, StatusEnum.CONSIDERATION)
        update_user(user)
        return make_response("OK", 200)
    except Exception as e:
        log.error(f"Ошибка подачи на вакансию на hh.ru: {e}")
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/test", methods=["POST"])
def test():
    log.info(request.json)
    login = request.json["login"]
    log.info(f"login: {login}")
    password = request.json["password"]
    user = getUser(login)
    log.info(f"User: {user.__str__()}")
    return make_response(user.to_json(default=json_serial), 200)


@app.route("/add", methods=["POST"])
def add():
    user = UserModel(login="test", password="test")
    saveUser(user)
    return make_response(user.to_json(default=json_serial), 200)


# Configure upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        data = request
        if "file" not in request.files:
            return (
                jsonify(
                    {
                        "message": "No file part in the request or no data in request"
                    }
                ),
                400,
            )

        file = request.files["file"]
        login = data.form.get("login")
        password = data.form.get("password")

        if file.filename == "":
            return jsonify({"message": "No file selected"}), 400

        if file:
            file_path = os.path.join(
                app.config["UPLOAD_FOLDER"], f"{login}.pdf"
            )
            file.save(file_path)
            log.info(file_path)
            user = parse(file_path)
            # user = UserModel(login=login, password=password, first_name="Daria", phone="890", email="sdklal@dlsfj")
            log.info(user.__str__)
            user.login = login
            user.password = password
            update_user(user)
            return jsonify(user.to_json()), 200
        log.error("file upload failed")
        return jsonify({"message": "File upload failed"}), 500

    except Exception as e:
        log.error(f"Ошибка загрузки резюме: {e}", exc_info=True)
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/form/update", methods=["POST"])
def update_form():
    try:
        data = request.json
        if not data or "login" not in data or "password" not in data:
            return make_response(
                jsonify(
                    {
                        "error": "Invalid request. 'login', 'password' fields are "
                                 "required."
                    }
                ),
                400,
            )

        user = UserModel.from_json(request.data)
        log.info(f"User: {user}")
        hh_token = get_hh_token(user.login)
        update_resume(user, hh_token.access_token)
        user_cases.updateUser(user)
        return make_response("OK", 200)
    except Exception as e:
        log.error(f"Ошибка сохранения данных из формы: {e}")
        return make_response(jsonify({"error": str(e)}), 500)
