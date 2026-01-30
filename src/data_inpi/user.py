import os
from pathlib import Path
import logging

# Configurez le logging ici ou assurez-vous qu'il est configuré ailleurs
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class UserMangement:

    def __init__(self, app_name=".DataINPI_App"):
        # Le nom du dossier caché de l'application
        self.app_name = app_name
        # Répertoire personnel de l'utilisateur (le plus fiable)
        self._user_home = Path.home()
        # Chemin complet vers le dossier de données de l'application
        self._app_data_dir = self._user_home / self.app_name

        # S'assurer que le dossier de l'application existe lors de l'initialisation
        self._ensure_app_data_dir_exists()

    def get_user_home(self) -> str:
        """
        Retourne le chemin absolu du répertoire personnel de l'utilisateur.
        """
        return str(self._user_home)

    def get_app_data_dir(self) -> str:
        """
        Retourne le chemin absolu du dossier de données de l'application (ex: ~/.DataINPI_App).
        """
        return str(self._app_data_dir)

    def _ensure_app_data_dir_exists(self):
        """
        Crée le dossier de l'application s'il n'existe pas.
        """
        try:
            self._app_data_dir.mkdir(parents=True, exist_ok=True)
            logging.info(
                f"Dossier de données de l'application prêt : {self._app_data_dir}"
            )
        except Exception as e:
            logging.error(
                f"Erreur fatale : Impossible de créer le dossier de données ({self._app_data_dir}): {e}"
            )
            # Il est crucial que l'application ne plante pas ici, mais on signale l'erreur
            # Dans une application réelle, on pourrait empêcher l'écriture.
            pass

    # Votre méthode existante, utilisant Path.home() qui est plus sûr que os.environ
    def get_downloads_folder(self) -> str:
        """
        Tente de déterminer le chemin par défaut du dossier Téléchargements.
        """
        # home est déjà défini dans __init__
        downloads_path = self._user_home / "Downloads"

        # Vérification rapide (Pathlib est plus propre)
        if downloads_path.is_dir():
            return str(downloads_path)

        # Solution de repli (retourne le bureau si Downloads n'est pas trouvé)
        logging.warning(
            "Dossier 'Downloads' non trouvé. Retourne le chemin du 'Desktop'."
        )
        return str(self._user_home / "Desktop")
