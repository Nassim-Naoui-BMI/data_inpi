import pandas as pd
from typing import List, Dict, Any
import os
import json


class DataCleaning:

    def __init__(self):
        """
        Initialise l'objet DataCleaning en lisant le fichier de données.

        Args:
            file_path (str): Le chemin vers le fichier de données.
            file_type (str): Le type de fichier ('csv', 'excel', 'json', etc.).
            export_path (str): Le chemin du dossier où exporter le fichier.
        """
        # self.file_path = self.file_path
        # self.file_type = self.file_type
        # self.df = self.read_file()

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

    # -----------------------------------------------------------------------------------

    def get_name_siren_arrays():
        """
        stock les noms d'entreprise et les siren dans arrays distincts.
        """

    # -----------------------------------------------------------------------------------

    def export_etablissements_to_excel(
        self,
        data_entreprises: List[Dict[str, Any]],
        directory,
        file_name: str = "export_etablissements.xlsx",
        principaux_sheet: str = "Etablissements_Principaux",
        secondaires_sheet: str = "Autres_Etablissements",
    ) -> None:

        principaux_data = []
        autres_etablissements_data = []

        print(f"Démarrage du traitement et de l'exportation vers {file_name}...")

        for entreprise in data_entreprises:

            if not isinstance(entreprise, dict):
                print(
                    f"⚠️ Avertissement : Un élément n'est pas un dictionnaire (type: {type(entreprise).__name__}). Ignoré."
                )
                continue

            # Traitement de l'établissement principal
            principal = entreprise.copy()
            # On retire la clé des secondaires avant d'ajouter le principal au DataFrame
            if "autresEtablissementsTrouves" in principal:
                del principal["autresEtablissementsTrouves"]
            principaux_data.append(principal)

            # Traitement des établissements secondaires
            # Utilisation de .get() avec une liste vide comme valeur par défaut []
            etablissements_actifs = entreprise.get("autresEtablissementsTrouves", [])

            for etablissement in etablissements_actifs:
                # AUCUNE MODIFICATION : On ajoute l'établissement tel quel
                autres_etablissements_data.append(etablissement.copy())

        # Création et Exportation des DataFrames (le reste est inchangé)
        df_principaux = pd.DataFrame(principaux_data)
        df_secondaires = pd.DataFrame(autres_etablissements_data)

        df_principaux = df_principaux.loc[
            :,
            [
                "siren",
                "siret",
                "denomination",
                "formeJuridique",
                "codeApe",
                "nbAutresEtablissementsTrouves",
                "numVoie",
                "typeVoie",
                "voie",
                "commune",
                "complementLocalisation",
                "codePostal",
                "pays",
            ],
        ]

        df_secondaires = df_secondaires.loc[
            :,
            [
                "siren",
                "siret",
                "enseigne",
                "formeJuridique",
                "codeApe",
                "dateEffetFermeture",
                "numVoie",
                "typeVoie",
                "voie",
                "commune",
                "complementLocalisation",
                "codePostal",
                "pays",
            ],
        ]

        if df_principaux.empty and df_secondaires.empty:
            print(
                "❌ Échec de l'exportation : Aucun établissement valide n'a été trouvé après le traitement."
            )
            return

        try:
            with pd.ExcelWriter(
                directory + "/" + file_name, engine="openpyxl"
            ) as writer:
                df_principaux.to_excel(writer, sheet_name=principaux_sheet, index=False)
                df_secondaires.to_excel(
                    writer, sheet_name=secondaires_sheet, index=False
                )

            print(f"✅ Exportation terminée avec succès : {file_name}")

        except Exception as e:
            print(f"❌ Erreur critique lors de l'export Excel : {e}")
