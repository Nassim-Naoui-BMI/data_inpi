import requests
import json
import time


class ApiRequest:

    def __init__(self, auth_url, api_url, username, password):
        """
        Initialise l'objet ApiRequest avec les informations d'authentification.

        Args:
            auth_url (str): L'URL d'authentification de l'API.
            username (str): L'identifiant client pour l'authentification.
            password (str): Le secret client pour l'authentification.
        """
        self.auth_url = auth_url
        self.api_url = api_url
        self.username = username
        self.password = password
        self.access_token = self._load_token()

    def _load_token(self):
        """
        Charge un jeton d'accès depuis un fichier s'il est encore valide.
        """
        try:
            with open("./src/token_dir/token.json", "r") as f:
                token_data = json.load(f)
                if time.time() < token_data.get("expires_at", 0) and token_data.get(
                    "access_token"
                ):
                    return token_data.get("access_token")
        except (FileNotFoundError, json.JSONDecodeError):
            return None
        return None

    def _save_token(self, token_data):
        """
        Sauvegarde le token dans un fichier json
        """
        token_data["expires_at"] = time.time() + 3600
        with open("./src/token_dir/token.json", "w") as f:
            json.dump(token_data, f, indent=2)

    def _get_expiration_time(self):
        """
        Méthode utilitaire pour obtenir le temps d'expiration du token.
        """
        try:
            with open("./src/token_dir/token.json", "r") as f:
                token_data = json.load(f)
                return token_data.get("expires_at", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0

    def get_access_token(self):
        """
        Récupère un jeton d'accès pour l'API RNE en utilisant le flux d'authentification SSO.
        """

        if self.access_token and time.time() < self._get_expiration_time():
            return self.access_token

        try:
            response = requests.post(
                self.auth_url,
                json={
                    "username": self.username,
                    "password": self.password,
                },
            )
            response.raise_for_status()
            token_data = response.json()

            token = token_data.get("token") or token_data.get("access_token")
            if not token:
                raise ValueError("Aucun jeton d'accès trouvé dans la réponse de l'API.")

            self._save_token({"access_token": token})
            return self.access_token

        except requests.exceptions.HTTPError as e:
            # Gestion des erreurs de type 4xx ou 5xx
            print(
                f"Erreur HTTP lors de l'obtention du jeton: {e.response.status_code} - {e.response.text}"
            )
            return None
        except requests.exceptions.RequestException as e:
            # Gestion des erreurs de connexion ou de timeout
            print(f"Erreur de connexion lors de l'obtention du jeton: {e}")
            return None
        except ValueError:
            # Erreur si la réponse n'est pas un JSON valide
            print(
                "Erreur de décodage JSON: la réponse du serveur n'est pas un JSON valide."
            )
            return None

    def search_company_by_name(self, access_token, company_name):
        """
        Recherche une entreprise dans l'API RNE en utilisant le jeton d'accès.
        """

        if not access_token:
            print("Erreur: Jeton d'accès non valide. Impossible de procéder.")
            return None

        api_url = self.api_url
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"companyName": company_name}

        try:
            response = requests.get(api_url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                retry_after_value = e.response.headers.get("Retry-After")
                if retry_after_value:
                    print(
                        f" ⚠️ Erreur HTTP lors de la recherche: {e.response.status_code} - {e.response.text} - temps d'attente: {retry_after_value}"
                    )
                else:
                    print(
                        f"⚠️ Erreur HTTP lors de la recherche: {e.response.status_code} - {e.response.text} - temps d'attente: non communiqué"
                    )
            else:
                print(
                    f"Erreur HTTP lors de la recherche: {e.response.status_code} - {e.response.text}"
                )
        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion lors de la recherche: {e}")
        except ValueError:
            print(
                "Erreur de décodage JSON: la réponse du serveur n'est pas un JSON valide."
            )
        return None

    def search_company_by_siren(self, access_token, siren):
        """
        Recherche une entreprise dans l'API RNE en utilisant le jeton d'accès.
        """

        if not access_token:
            print("Erreur: Jeton d'accès non valide. Impossible de procéder.")
            return None

        api_url = f"https://registre-national-entreprises.inpi.fr/api/companies/{siren}"
        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:

                retry_after_value = e.response.headers.get("Retry-After")
                if retry_after_value:
                    print(
                        f" ⚠️ Erreur HTTP lors de la recherche: {e.response.status_code} - {e.response.text} - temps d'attente: {retry_after_value}"
                    )
                else:
                    print(
                        f"⚠️ Erreur HTTP lors de la recherche: {e.response.status_code} - {e.response.text} - temps d'attente: non communiqué"
                    )
            else:
                print(
                    f"Erreur HTTP lors de la recherche: {e.response.status_code} - {e.response.text}"
                )
        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion lors de la recherche: {e}")
        except ValueError:
            print(
                "Erreur de décodage JSON: la réponse du serveur n'est pas un JSON valide."
            )
        return None
