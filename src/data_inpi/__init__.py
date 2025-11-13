import os
import sys
from flask import Flask
from flask_cors import CORS
from .routes import bp as routes_bp
from .config import Config


# Fonction utilitaire pour déterminer le chemin de la racine du projet,
# compatible avec les environnements normaux et les exécutables PyInstaller.
def get_base_path():
    """
    Détermine le chemin racine de l'application.
    """
    if getattr(sys, 'frozen', False):
        # Chemin dans l'exécutable PyInstaller
        return sys._MEIPASS
    else:
        # Chemin en mode développement
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(current_dir, '..', '..'))


def create_app():
    # 1. Déterminer le chemin de la racine
    base_path = get_base_path()

    # Le dossier UI est directement à la racine
    template_dir = os.path.join(base_path, 'UI')
    static_dir = os.path.join(base_path, 'UI')
    
    # DEBUG : Affiche le chemin utilisé (vérification)
    print(f"DEBUG PATH: Base Path utilisé: {base_path}")
    print(f"DEBUG PATH: Template/Static directory : {template_dir}")
    
    # 2. Configurer Flask avec les chemins personnalisés
    app = Flask(
        __name__,
        # Flask cherchera les fichiers HTML ici
        template_folder=template_dir, 
        # Flask cherchera les fichiers JS/CSS ici (si tout est dans 'UI')
        static_folder=static_dir  
    )
    
    app.config.from_object(Config)
    CORS(app)
    app.register_blueprint(routes_bp)
    
    return app