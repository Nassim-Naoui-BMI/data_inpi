from data_inpi import JsonHandler, ApiRequest, DataCleaning
import os
import json
import pandas as pd

auth_url = "https://registre-national-entreprises.inpi.fr/api/sso/login"
username = os.environ.get("INPI_CLIENT_ID")
password = os.environ.get("INPI_CLIENT_SECRET")


if __name__ == "__main__":
    connexion = ApiRequest(auth_url, username, password)
    token = connexion.get_access_token()
    company_data = connexion.search_company_by_siren(token, 301468146)
    company_data_clean = [JsonHandler.flatten_json_siren(company_data)]
    JsonHandler.create_json_file(company_data_clean)
    cleaner = DataCleaning()
    cleaner.export_etablissements_to_excel(
        data_entreprises=company_data_clean,
        file_name="rapport_final_etablissements.xlsx",
    )
