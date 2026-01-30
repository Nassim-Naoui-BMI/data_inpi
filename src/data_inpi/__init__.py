import os
import sys
from flask import Flask
from flask_cors import CORS
from .routes import bp as routes_bp
from .config import Config


# ----------------------------------------------------
# NOUVELLE FONCTION CLÉ pour la compatibilité PyInstaller
# ----------------------------------------------------
def resource_path(relative_path):
    """
    Détermine le chemin absolu vers la ressource, fonctionne pour le mode dev et l'exécutable PyInstaller.
    """
    try:
        # PyInstaller stocke le chemin racine dans _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Chemin normal en mode développement (la racine du projet)
        # On remonte de 'data_inpi' vers la racine du projet (où se trouve 'UI')
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    return os.path.join(base_path, relative_path)


# ----------------------------------------------------


def create_app():
    # 1. Déterminer les chemins des dossiers 'UI'
    # Le chemin est construit à partir de la racine déterminée par resource_path,
    # en supposant que le dossier 'UI' se trouve à la racine du projet/bundle.

    # 🚨 Hypothèse: Le dossier 'UI' est à la racine du projet.
    template_dir = resource_path("UI")
    static_dir = resource_path("UI")

    # DEBUG : Affiche le chemin utilisé (vérification)
    print(f"DEBUG PATH: Template/Static directory: {template_dir}")

    # 2. Configurer Flask avec les chemins personnalisés
    app = Flask(
        __name__,
        # Flask cherchera les fichiers HTML ici (e.g. index.html)
        template_folder=template_dir,
        # Flask cherchera les fichiers JS/CSS ici (si tout est dans 'UI')
        static_folder=static_dir,
        # Optionnel: Préciser l'URL pour les fichiers statiques (laisse par défaut si 'UI' contient le dossier 'static')
        # static_url_path='/static'
    )

    app.config.from_object(Config)
    CORS(app)
    app.register_blueprint(routes_bp)

    return app
