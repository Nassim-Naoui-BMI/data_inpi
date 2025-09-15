import json


class JsonHandler:

    def __init__(self, json_file):
        self.json_file = json_file
        self.data = self.load_json()

    def reand_load_json(self):
        with open(self.json_file, "r") as f:
            return json.load(f)

    def print_json(self, data):
        print(f"Clean object : ${json.dumps(data, indent=2)}")

    def flatten_json(self, data):
        new_obj = (
            {
                "denomination": data[0]["formality"]["content"]["personneMorale"][
                    "identite"
                ]["entreprise"]["denomination"],
                "siren": data[0]["formality"]["content"]["personneMorale"]["identite"][
                    "entreprise"
                ]["siren"],
                "siret": data[0]["formality"]["content"]["personneMorale"][
                    "etablissementPrincipal"
                ]["descriptionEtablissement"]["siret"],
                "codeApe": data[0]["formality"]["content"]["personneMorale"][
                    "identite"
                ]["entreprise"]["codeApe"],
                "formeJuridique": data[0]["formality"]["content"]["personneMorale"][
                    "identite"
                ]["entreprise"]["formeJuridique"],
                "dateDebutActiv": data[0]["formality"]["content"]["personneMorale"][
                    "identite"
                ]["entreprise"]["dateDebutActiv"],
                "pays": data[0]["formality"]["content"]["personneMorale"][
                    "etablissementPrincipal"
                ]["adresse"]["pays"],
                "numVoie": data[0]["formality"]["content"]["personneMorale"][
                    "etablissementPrincipal"
                ]["adresse"]["numVoie"],
                "typeVoie": data[0]["formality"]["content"]["personneMorale"][
                    "etablissementPrincipal"
                ]["adresse"]["typeVoie"],
                "voie": data[0]["formality"]["content"]["personneMorale"][
                    "etablissementPrincipal"
                ]["adresse"]["voie"],
                "complementLocalisation": data[0]["formality"]["content"][
                    "personneMorale"
                ]["etablissementPrincipal"]["adresse"]["complementLocalisation"],
                "codePostal": data[0]["formality"]["content"]["personneMorale"][
                    "etablissementPrincipal"
                ]["adresse"]["codePostal"],
                "commune": data[0]["formality"]["content"]["personneMorale"][
                    "etablissementPrincipal"
                ]["adresse"]["commune"],
                "societeEtrangere": data[0]["formality"]["content"]["natureCreation"][
                    "societeEtrangere"
                ],
            },
        )

        return new_obj
