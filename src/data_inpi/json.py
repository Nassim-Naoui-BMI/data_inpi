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
        content_keys = data[index]["formality"]["content"].keys()
        type_person = (
            "personneMorale" if "personneMorale" in content_keys else "personnePhysique"
        )

        new_obj = (
            {
                "denomination": data[index]["formality"]["content"][type_person][
                    "identite"
                ]["entreprise"]["denomination"],
                "siren": data[index]["formality"]["content"][type_person]["identite"][
                    "entreprise"
                ]["siren"],
                "nicSiege": data[index]["formality"]["content"][type_person][
                    "identite"
                ]["entreprise"]["nicSiege"],
                "codeApe": data[index]["formality"]["content"][type_person]["identite"][
                    "entreprise"
                ]["codeApe"],
                "formeJuridique": data[index]["formality"]["content"][type_person][
                    "identite"
                ]["entreprise"]["formeJuridique"],
                "pays": data[index]["formality"]["content"][type_person][
                    "adresseEntreprise"
                ]["adresse"]["pays"],
                "numVoie": (
                    data[index]["formality"]["content"][type_person][
                        "adresseEntreprise"
                    ]["adresse"]["numVoie"]
                    if data[index]["formality"]["content"][type_person][
                        "adresseEntreprise"
                    ]["adresse"]["numVoiePresent"]
                    else None
                ),
                "typeVoie": data[index]["formality"]["content"][type_person][
                    "adresseEntreprise"
                ]["adresse"]["typeVoie"],
                "voie": data[index]["formality"]["content"][type_person][
                    "adresseEntreprise"
                ]["adresse"]["voie"],
                "complementLocalisation": (
                    data[index]["formality"]["content"][type_person][
                        "adresseEntreprise"
                    ]["adresse"]["complementLocalisation"]
                    if data[index]["formality"]["content"][type_person][
                        "adresseEntreprise"
                    ]["adresse"]["complementLocalisationPresent"]
                    else None
                ),
                "codePostal": data[index]["formality"]["content"][type_person][
                    "adresseEntreprise"
                ]["adresse"]["codePostal"],
                "commune": data[index]["formality"]["content"][type_person][
                    "adresseEntreprise"
                ]["adresse"]["commune"],
            },
        )

        new_obj[0]["siret"] = new_obj[0]["siren"] + new_obj[0]["nicSiege"]
        return new_obj

    def create_json_file(data):
        with open("samse_draft.json", "w") as f:
            json.dump(data, f, indent=2)
