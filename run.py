import os
import logging
import webbrowser  # Requis pour ouvrir le navigateur
import threading   # Requis pour lancer le navigateur sans bloquer le serveur
from data_inpi import create_app
from dotenv import load_dotenv
from waitress import serve

# 1. Configuration initiale du logger (à placer au début du script)
logging.basicConfig(level=logging.INFO)

load_dotenv(".flaskenv")

app = create_app()

if __name__ == "__main__":
    # --- Configuration du Lancement ---
    
    # On utilise 127.0.0.1 (localhost) pour un exécutable local.
    # Cela évite les popups de pare-feu Windows.
    HOST_IP = '127.0.0.1'
    PORT = 5000
    APP_URL = f"http://{HOST_IP}:{PORT}"

    # 2. Configurer spécifiquement le logger de Waitress pour plus de verbosité
    waitress_logger = logging.getLogger('waitress')
    waitress_logger.setLevel(logging.INFO) 

    # 3. Fonction pour ouvrir le navigateur
    def open_browser():
        """ Ouvre le navigateur par défaut après un court délai. """
        try:
            webbrowser.open(APP_URL)
        except Exception as e:
            print(f"Erreur lors de l'ouverture du navigateur : {e}")

    # 4. Lancer l'ouverture du navigateur dans un thread séparé
    # Nous utilisons un Timer pour donner 2 secondes au serveur pour démarrer
    # avant que le navigateur ne tente de s'y connecter.
    print(f"Le serveur démarre. Ouverture du navigateur sur {APP_URL} dans 2 secondes...")
    threading.Timer(2.0, open_browser).start()

    # 5. Lancement du serveur (cette fonction est bloquante)
    print(f"Démarrage du serveur web Waitress sur {APP_URL}...")
    serve(
        app, 
        host=HOST_IP, 
        port=PORT
    )