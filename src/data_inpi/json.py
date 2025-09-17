import json


class JsonHandler:

    def __init__(self):
        pass

    def reand_load_json(self, file):
        with open(file, "r") as f:
            data = json.load(f)
            return data

    def print_json(self, data):
        print(f"Clean object : ${json.dumps(data, indent=2)}")

    def flatten_json(self, data, index):

        morale_obj = data[index]["formality"]["content"].get("personneMorale", {})

        if morale_obj:
            denomination = morale_obj["identite"]["entreprise"]["denomination"]
            siren = morale_obj["identite"]["entreprise"]["siren"]
            nicSiege = morale_obj["identite"]["entreprise"]["nicSiege"]
            codeApe = morale_obj["identite"]["entreprise"]["codeApe"]
            formeJuridique = morale_obj["identite"]["entreprise"]["formeJuridique"]
            pays = morale_obj["adresseEntreprise"]["adresse"]["pays"]
            numVoie = morale_obj["adresseEntreprise"]["adresse"].get("numVoie", None)
            typeVoie = morale_obj["adresseEntreprise"]["adresse"].get("typeVoie", None)
            voie = morale_obj["adresseEntreprise"]["adresse"].get("voie", None)
            complementLocalisation = morale_obj["adresseEntreprise"]["adresse"].get(
                "complementLocalisation", None
            )
            codePostal = morale_obj["adresseEntreprise"]["adresse"].get(
                "codePostal", None
            )
            commune = morale_obj["adresseEntreprise"]["adresse"].get("commune", None)
        else:
            physique_obj = data[index]["formality"]["content"].get(
                "personnePhysique", {}
            )
            nom = physique_obj["identite"]["entrepreneur"]["descriptionPersonne"]["nom"]
            prenom_list = physique_obj["identite"]["entrepreneur"][
                "descriptionPersonne"
            ]["prenoms"]
            prenom = ",".join(prenom_list)
            denomination = nom + " " + prenom
            siren = physique_obj["identite"]["entreprise"]["siren"]
            nicSiege = physique_obj["identite"]["entreprise"]["nicSiege"]
            codeApe = physique_obj["identite"]["entreprise"]["codeApe"]
            formeJuridique = physique_obj["identite"]["entreprise"].get(
                "formeJuridique", None
            )
            pays = physique_obj["adresseEntreprise"]["adresse"]["pays"]
            numVoie = physique_obj["adresseEntreprise"]["adresse"].get("numVoie", None)
            typeVoie = physique_obj["adresseEntreprise"]["adresse"].get(
                "typeVoie", None
            )
            voie = physique_obj["adresseEntreprise"]["adresse"].get("voie", None)
            complementLocalisation = physique_obj["adresseEntreprise"]["adresse"].get(
                "complementLocalisation", None
            )
            codePostal = physique_obj["adresseEntreprise"]["adresse"].get(
                "codePostal", None
            )
            commune = physique_obj["adresseEntreprise"]["adresse"].get("commune", None)

        siret = siren + nicSiege

        new_obj = {
            "denomination": denomination,
            "siren": siren,
            "siret": siret,
            "codeApe": codeApe,
            "formeJuridique": formeJuridique,
            "pays": pays,
            "numVoie": numVoie,
            "typeVoie": typeVoie,
            "voie": voie,
            "complementLocalisation": complementLocalisation,
            "codePostal": codePostal,
            "commune": commune,
        }

        return new_obj

    def create_json_file(self, data):
        with open("samse_draft.json", "w") as f:
            json.dump(data, f, indent=2)
