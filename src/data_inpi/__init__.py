import requests
import os
import json

def get_access_token():
    """
    Récupère un jeton d'accès pour l'API RNE en utilisant le flux d'authentification SSO.
    """
    auth_url = "https://registre-national-entreprises.inpi.fr/api/sso/login"
    username = os.environ.get("INPI_CLIENT_ID")
    password = os.environ.get("INPI_CLIENT_SECRET")

    if not username or not password:
        print("Erreur: Les variables d'environnement 'INPI_CLIENT_ID' et 'INPI_CLIENT_SECRET' ne sont pas définies.")
        return None

    auth_data = {
        "username": username,
        "password": password
    }

    try:
        
        response = requests.post(auth_url, json=auth_data)
        response.raise_for_status()
        token_data = response.json()
        
        
        return token_data.get("token") or token_data.get("access_token")
    except requests.exceptions.HTTPError as e:
        print(f"Erreur HTTP lors de l'obtention du jeton: {e.response.status_code} - {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion lors de l'obtention du jeton: {e}")
    except ValueError:
        print("Erreur de décodage JSON: la réponse du serveur n'est pas un JSON valide.")
    return None

def search_company(access_token, company_name):
    """
    Recherche une entreprise dans l'API RNE en utilisant le jeton d'accès.
    """
    if not access_token:
        print("Erreur: Jeton d'accès non valide. Impossible de procéder.")
        return None

    api_url = "https://registre-national-entreprises.inpi.fr/api/companies"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "companyName": company_name
    }

    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Erreur HTTP lors de la recherche: {e.response.status_code} - {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion lors de la recherche: {e}")
    except ValueError:
        print("Erreur de décodage JSON: la réponse du serveur n'est pas un JSON valide.")
    return None

if __name__ == "__main__":
    token = get_access_token()
    if token:
        company_to_search = "BMI GROUP FRANCE"
        company_data = search_company(token, company_to_search)
        if company_data:
            print(f"Résultats pour '{company_to_search}':")
            print(json.dumps(company_data, indent=2, ensure_ascii=False))
