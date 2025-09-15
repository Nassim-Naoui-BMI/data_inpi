from data_inpi import ApiRequest, DataCleaning, JsonHandler
import os
import json

auth_url = "https://registre-national-entreprises.inpi.fr/api/sso/login"
username = os.environ.get("INPI_CLIENT_ID")
password = os.environ.get("INPI_CLIENT_SECRET")


if __name__ == "__main__":
    # connexion = ApiRequest(auth_url, username, password)
    # token = connexion.get_access_token()
    # company_data = connexion.search_company_by_name(token, "BMI GROUP FRANCE")
    # print(json.dumps(company_data, indent=2, sort_keys=True))
    # with open("json_draft.json", "r") as f:
    # data = json.load(f)
    # new_obj = flatten_json(data)
    # print(f"Clean object : ${json.dumps(new_obj, indent=2)}")
    print("hellow world")
