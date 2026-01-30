import requests
import json
import time
import os
import logging
import urllib3
from pathlib import Path

# Importer la classe de gestion des utilisateurs
# Cette importation suppose que user_management.py est dans le même dossier que api.py
from .user import UserMangement

# Configuration du logging (si non fait globalement)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- INITIALISATION DE USER MANAGEMENT ET DÉFINITION DU CHEMIN ---

# 1. Initialiser le manager pour qu'il crée le dossier de l'application
user_manager = UserMangement()

# 2. Définir le chemin absolu du token via le manager
# On utilise Pathlib pour joindre le chemin du dossier à 'token.json'
TOKEN_FILE_PATH = Path(user_manager.get_app_data_dir()) / "token.json"

# Désactiver les avertissements SSL (si nécessaire pour le débogage)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- FIN DE LA LOGIQUE DE CHEMIN ---


class ApiRequest:

    def __init__(self, auth_url, api_url, username, password):
        """
        Initialise l'objet ApiRequest avec les informations d'authentification.
        """
        self.auth_url = auth_url
        self.api_url = api_url
        self.username = username
        self.password = password
        self.access_token = self._load_token()

    # --------------------------------------------------------------------------------------------------------

    def _load_token(self):
        """
        Charge un jeton d'accès depuis le chemin absolu TOKEN_FILE_PATH.
        """
        try:
            # Utilisation de TOKEN_FILE_PATH (qui est un objet Path)
            with open(TOKEN_FILE_PATH, "r") as f:
                token_data = json.load(f)
                if time.time() < token_data.get("expires_at", 0) and token_data.get(
                    "access_token"
                ):
                    return token_data.get("access_token")
        except (FileNotFoundError, json.JSONDecodeError):
            logging.warning(f"Fichier token non trouvé ou invalide à {TOKEN_FILE_PATH}")
            return None
        except Exception as e:
            logging.error(f"Erreur lors du chargement du token : {e}")
            return None
        return None

    def _save_token(self, token_data):
        """
        Sauvegarde le token dans le chemin absolu TOKEN_FILE_PATH.
        """
        try:
            # Durée de vie du token (ex: 1 heure)
            token_data["expires_at"] = time.time() + 3600
            # Utilisation de TOKEN_FILE_PATH
            with open(TOKEN_FILE_PATH, "w") as f:
                json.dump(token_data, f, indent=2)
            logging.info(f"Token sauvegardé dans {TOKEN_FILE_PATH}")
        except Exception as e:
            logging.error(
                f"Impossible de sauvegarder le token dans {TOKEN_FILE_PATH}: {e}"
            )
            logging.error(
                "L'application continuera, mais le token ne sera pas persisté."
            )

    # --------------------------------------------------------------------------------------------------------

    def _get_expiration_time(self):
        """
        Méthode utilitaire pour obtenir le temps d'expiration du token.
        """
        try:
            # Utilisation de TOKEN_FILE_PATH
            with open(TOKEN_FILE_PATH, "r") as f:
                token_data = json.load(f)
                return token_data.get("expires_at", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0

    # --------------------------------------------------------------------------------------------------------

    def get_access_token(self):
        """
        Récupère un jeton d'accès pour l'API RNE.
        """

        if self.access_token and time.time() < self._get_expiration_time():
            return self.access_token

        try:
            # Tentative d'authentification
            response = requests.post(
                self.auth_url,
                json={
                    "username": self.username,
                    "password": self.password,
                },
                # verify=False est utilisé temporairement pour les problèmes de certificats dans l'EXE
                verify=False,
            )

            response.raise_for_status()
            token_data = response.json()

            token = token_data.get("token") or token_data.get("access_token")
            if not token:
                raise ValueError("Aucun jeton d'accès trouvé dans la réponse de l'API.")

            self.access_token = token
            self._save_token({"access_token": token})
            return self.access_token

        except requests.exceptions.HTTPError as e:
            logging.error(
                f"Erreur HTTP lors de l'obtention du jeton: {e.response.status_code} - {e.response.text}"
            )
            raise e
        except requests.exceptions.RequestException as e:
            logging.error(f"Erreur de connexion lors de l'obtention du jeton: {e}")
            raise e
        except Exception as e:
            logging.error(f"Erreur inattendue (get_access_token): {e}")
            raise e

    # --------------------------------------------------------------------------------------------------------

    def search_company_by_name(self, access_token, company_name):
        """
        Recherche une entreprise dans l'API RNE en utilisant le jeton d'accès.
        """

        if not access_token:
            logging.error("Erreur: Jeton d'accès non valide.")
            raise ValueError("Jeton d'accès non valide. Impossible de procéder.")

        api_url = self.api_url
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"companyName": company_name}

        try:
            response = requests.get(
                api_url, headers=headers, params=params, verify=False
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            logging.error(
                f"Erreur HTTP (search_company_by_name): {e.response.status_code} - {e.response.text}"
            )
            raise e
        except requests.exceptions.RequestException as e:
            logging.error(f"Erreur de connexion (search_company_by_name): {e}")
            raise e
        except Exception as e:
            logging.error(f"Erreur inattendue (search_company_by_name): {e}")
            raise e

    # --------------------------------------------------------------------------------------------------------

    def search_company_by_siren(self, access_token, siren: str):
        """
        Recherche une entreprise dans l'API RNE en utilisant le jeton d'accès.
        """

        if not access_token:
            logging.error("Erreur: Jeton d'accès non valide.")
            raise ValueError("Jeton d'accès non valide. Impossible de procéder.")

        api_url = f"https://registre-national-entreprises.inpi.fr/api/companies/{siren}"
        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            response = requests.get(api_url, headers=headers, verify=False)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            logging.error(
                f"Erreur HTTP (search_company_by_siren): {e.response.status_code} - {e.response.text}"
            )
            raise e
        except requests.exceptions.RequestException as e:
            logging.error(f"Erreur de connexion (search_company_by_siren): {e}")
            raise e
        except Exception as e:
            logging.error(f"Erreur inattendue (search_company_by_siren): {e}")
            raise e
