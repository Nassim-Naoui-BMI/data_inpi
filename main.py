from data_inpi import JsonHandler, ApiRequest, DataCleaning
import os
import json

auth_url = "https://registre-national-entreprises.inpi.fr/api/sso/login"
username = os.environ.get("INPI_CLIENT_ID")
password = os.environ.get("INPI_CLIENT_SECRET")


if __name__ == "__main__":
    connexion = ApiRequest(auth_url, username, password)
    token = connexion.get_access_token()
    company_data = connexion.search_company_by_name(token, "SAMSE")
    data = []
    if company_data:
        for i in range(0, len(company_data)):
            temp_data = JsonHandler().flatten_json(company_data, i)
            data.append(temp_data)
        print(f"Len data : {len(company_data)}")
        print(f"Len new_obj : {len(data)}")
        JsonHandler().print_json(data)
