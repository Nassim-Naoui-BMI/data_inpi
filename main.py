from data_inpi import ApiRequest, DataCleaning
import os
import json

auth_url = "https://registre-national-entreprises.inpi.fr/api/sso/login"
username = os.environ.get("INPI_CLIENT_ID")
password = os.environ.get("INPI_CLIENT_SECRET")


if __name__ == "__main__":
    connexion = ApiRequest(auth_url, username, password)
    token = connexion.get_access_token()
    company_data = connexion.search_company_by_name(token, "BMI GROUP FRANCE")
    print(json.dumps(company_data, indent=2, sort_keys=True))
