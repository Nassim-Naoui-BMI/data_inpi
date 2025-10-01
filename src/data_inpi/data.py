import pandas as pd
import os
import json


class DataCleaning:

    def __init__(self, file_path, file_type):
        """
        Initialise l'objet DataCleaning en lisant le fichier de données.

        Args:
            file_path (str): Le chemin vers le fichier de données.
            file_type (str): Le type de fichier ('csv', 'excel', 'json', etc.).
            export_path (str): Le chemin du dossier où exporter le fichier.
        """
        self.file_path = file_path
        self.file_type = file_type
        self.df = self.read_file()

    def read_file(self):
        """
        Lit le fichier et retourne un DataFrame pandas.
        """

        read_method = getattr(pd, f"read_{self.file_type}", None)

        if read_method:
            return read_method(self.file_path)
        else:
            raise ValueError(f"Type de fichier non supporté : {self.file_type}")

    def drop_na(self, axis=0, how="any"):
        """
        Supprime les valeurs manquantes (NaN) du DataFrame.
        """
        self.df = self.df.dropna(axis=axis, how=how)
        print("Les valeurs NaN ont été supprimées.")

    def export_to_excel(self, export_path, file_name="data-inpi-output.xlsx"):
        """
        Exporte le DataFrame nettoyé dans un fichier Excel.

        Args:
            export_path (str): Le chemin du dossier où exporter le fichier.
            file_name (str): Le nom du fichier Excel à créer.
        """
        full_path = os.path.join(export_path, file_name)

        self.df.to_excel(full_path, index=False)
        print(f"DataFrame exporté avec succès vers {full_path}")
