import os
from pathlib import Path


class UserMangement:

    def __init__(self):
        pass

    def get_downloads_folder(self):
        """
        Tente de déterminer le chemin par défaut du dossier Téléchargements.
        """
        # 1. Utiliser le dossier HOME de l'utilisateur
        home = Path.home()

        # 2. Construire le chemin vers "Downloads" (conventionnelle sur la plupart des OS)
        downloads_path = home / "Downloads"

        # Vérification rapide (au cas où l'utilisateur a renommé ou déplacé le dossier)
        if downloads_path.is_dir():
            return str(downloads_path)

        # Si non trouvé, essayer la méthode de Windows (si c'est Windows)
        # ou simplement retourner le HOME pour une solution de repli
        if os.name == "nt" and os.environ.get("USERPROFILE"):  # 'nt' pour Windows
            downloads_path = Path(os.environ["USERPROFILE"]) / "Downloads"
            if downloads_path.is_dir():
                return str(downloads_path)

        # Solution de repli (par exemple, sur le bureau)
        return str(home / "Desktop")
