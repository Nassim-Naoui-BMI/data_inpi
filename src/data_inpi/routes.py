from flask import Blueprint, jsonify, request, current_app, render_template
import os
import signal
import logging

from .config import Config
from .api import ApiRequest
from .json import JsonHandler
from .data import DataCleaning
from .user import UserMangement


bp = Blueprint("routes", __name__)


@bp.route("/")
def index():
    """Sert la page d'accueil (index.html) de l'application."""
    # Flask cherchera 'index.html' dans le dossier que nous avons
    # défini comme 'template_folder' (c'est-à-dire le dossier 'UI')
    return render_template("index.html")


@bp.route("/ping")
def ping():
    return jsonify({"status": "ok"})


@bp.route("/debug")
def debug_config():

    return {
        "auth_url": Config.auth_url,
        "api_url": Config.api_url,
        "username": Config.username,
        "password": Config.password,
    }


@bp.route("/token", methods=["GET"])
def get_token():

    try:
        api = ApiRequest(
            auth_url=Config.auth_url,
            api_url=Config.api_url,
            username=Config.username,
            password=Config.password,
        )

        token = api.get_access_token()

        # Si tout va bien, on renvoie le succès
        return jsonify({"status_access_token": "ok"})

    except Exception as e:
        # SI QUELQUE CHOSE PLANTE (ex: SSLError)
        # On logue l'erreur complète dans la console du serveur
        logging.error(
            f"Erreur critique lors de la récupération du token: {e}", exc_info=True
        )

        # On renvoie un JSON d'erreur clair au frontend
        # Le 'str(e)' contiendra la VRAIE erreur (ex: "SSLError: ...")
        return (
            jsonify({"error": "Échec de la récupération du token", "details": str(e)}),
            500,
        )


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


@bp.route("/getExcel", methods=["POST"])
def edit_excel():
    try:
        data_json = request.get_json()
    except:
        return {"error": "Le corps de la requête doit être un JSON valide"}, 400

    if data_json is None:
        return {"error": "Le JSON n'est pas fourni dans la requête."}, 400

    data_pour_export = data_json

    cleaner = DataCleaning()
    user = UserMangement()
    path = user.get_downloads_folder()

    cleaner.export_etablissements_to_excel(data_pour_export, path)

    return {"message": "Export Excel démarré avec succès."}, 200


@bp.route("/shutdown", methods=["POST"])
def shutdown_server():
    # Sécurité : N'accepter que les requêtes venant de la machine locale
    if request.remote_addr != "127.0.0.1":
        return jsonify({"error": "Non autorisé"}), 403

    print("Arrêt du serveur demandé...")

    # Envoyer le signal de terminaison au processus serveur actuel
    try:
        os.kill(os.getpid(), signal.SIGTERM)
        return jsonify({"message": "Serveur en cours d'arrêt..."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
