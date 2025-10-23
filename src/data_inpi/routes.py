from flask import Blueprint, jsonify, request, current_app

from .config import Config
from .api import ApiRequest
from .json import JsonHandler
from .data import DataCleaning
from .user import UserMangement


bp = Blueprint("routes", __name__)


@bp.route("/ping")
def ping():
    return jsonify({"status": "ok"})


@bp.route("/debug")
def debug_config():

    return {
        "auth_url": Config.auth_url,
        "username": Config.username,
    }


@bp.route("/token", methods=["GET"])
def get_token():

    api = ApiRequest(
        auth_url=Config.auth_url,
        api_url=Config.api_url,
        username=Config.username,
        password=Config.password,
    )

    token = api.get_access_token()

    return jsonify({"status access_token": "ok"})


@bp.route("/inpi/siren/<siren>", methods=["GET"])
def get_inpi_data_by_siren(siren):

    api = ApiRequest(
        auth_url=Config.auth_url,
        api_url=Config.api_url,
        username=Config.username,
        password=Config.password,
    )

    token = api.get_access_token()

    data = api.search_company_by_siren(access_token=token, siren=siren)

    cleaner = JsonHandler()
    cleanedData = cleaner.flatten_json_siren(data)

    return cleanedData


@bp.route("/inpi/name/<companyName>", methods=["GET"])
def get_inpi_data_by_name(companyName):

    api = ApiRequest(
        auth_url=Config.auth_url,
        api_url=Config.api_url,
        username=Config.username,
        password=Config.password,
    )

    token = api.get_access_token()

    list_company = []
    data = api.search_company_by_name(access_token=token, company_name=companyName)

    cleaner = JsonHandler()

    for i in range(0, len(data)):
        try:
            company_data_clean = cleaner.flatten_json_company_name(data, i)
            list_company.append(company_data_clean)
        except (KeyError, IndexError) as e:
            print(f"Erreur de traitement pour (index {i}): {e}")

    return list_company


bp.route("/getExcel", methods=["GET"])


def edit_excel(data):
    cleaner = DataCleaning()
    user = UserMangement()

    path = user.get_downloads_folder()

    cleaner()
