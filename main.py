from data_inpi import JsonHandler, ApiRequest, DataCleaning
import os
import json
import pandas as pd
import numpy as np
import datetime
import time

auth_url = "https://registre-national-entreprises.inpi.fr/api/sso/login"
username = os.environ.get("INPI_CLIENT_ID")
password = os.environ.get("INPI_CLIENT_SECRET")


if __name__ == "__main__":
    """
    Initialisation du Token
    """
    connexion = ApiRequest(auth_url, username, password)
    token = connexion.get_access_token()

    """
    Lecture du fichier et des onglets
    """
    customer_file = pd.read_excel(
        "./data_import/liste des tiers à vérifier.xlsx",
        sheet_name="liste raison social clients",
    )
    supplier_file = pd.read_excel(
        "./data_import/liste des tiers à vérifier.xlsx",
        sheet_name="liste raison social fournisseur",
    )
    siren_file = pd.read_excel(
        "./data_import/liste des tiers à vérifier.xlsx", sheet_name="liste SIREN"
    )

    """
    Isolation des noms et siren dans des arrays.
    """
    name_array = np.concatenate(
        (
            customer_file["Raison sociale"].unique(),
            supplier_file["Name 1 - NAME1"].unique(),
        )
    )
    siren_array = siren_file["Tax Number 2"].unique()

    """
    Boucle sur chaque éléments des arrays
    """
    list_company = []
    list_error = []

    print(f"Initialisation: ${datetime.datetime.now()}")

    for company_name in name_array:
        company_data = connexion.search_company_by_name(token, company_name)
        time.sleep(1)
        if company_data:
            for i in range(0, len(company_data)):
                try:
                    company_data_clean = JsonHandler.flatten_json_company_name(
                        company_data, i
                    )
                    list_company.append(company_data_clean)
                except (KeyError, IndexError) as e:
                    print(f"Erreur de traitement pour {company_name} (index {i}): {e}")
                    list_error.append(company_name)
            print(f"La compagnie: ${company_name} a bien été trouvé et stocké ✅")

    for company_siren in siren_array:
        company_data = connexion.search_company_by_siren(token, int(company_siren))
        time.sleep(1)
        if company_data:
            company_data_clean = JsonHandler.flatten_json_siren(company_data)
            list_company.append(company_data_clean)
            print(f"Le SIREN: ${company_siren} a bien été trouvé et stocké ✅")

    """
    Export en fichier excel
    """
    cleaner = DataCleaning()
    cleaner.export_etablissements_to_excel(
        data_entreprises=list_company,
        file_name="rapport_final_etablissements.xlsx",
    )

    print(f" error array: {list_error}")
    print(f"Fin d'exécution: ${datetime.datetime.now()}")
