from flask import Blueprint, jsonify, request

from .api import ApiRequest
from .data import DataCleaning
from .json import JsonHandler


bp = Blueprint("routes", __name__)


@bp.route("/ping")
def ping():
    return jsonify({"status": "ok"})
