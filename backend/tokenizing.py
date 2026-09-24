import json
import re

def clean_ingredient_name(name):
    # Puhdistaa/selkeyttää ainesosan nimen ennen tokenisointia
    name = name.lower().strip()

    # Poistetaan sulkeissa olevat tiedot
    name = re.sub(r"\([^)]*\)", "", name)

    # Poistetaan tuotemerkki
    # Useassa luki Pirkka, tänne voi lisätä myös muita tuttuja merkkejä
    name = re.sub(r"\bpirkka\b", "", name)

    # Poistetaan yleisiä kokoa kuvaavia sanoja
    # Näitäkin voi lisätä eteen sattuessa
    name = re.sub(r"\b(iso|suuri|pieni)\b", "", name)

    # Poistetaan ylimääräiset välilyönnit
    name = re.sub(r"\s+", " ", name).strip()

    return name

def tokenize_ingredient(name):
    return name.split()

# HUOM! Tähän pitää korvata oma json-reseptitiedosto
with open("<OMA-RESEPTI-JSON>", "r", encoding="utf-8") as f:
    recipes = json.load(f)

for recipe in recipes:
    for ingredient in recipe["ingredients"]:
        ingredient["clean_name"] = clean_ingredient_name(ingredient["name"])

        ingredient["tokens"] = tokenize_ingredient(ingredient["clean_name"])
        #print(ingredient["tokens"])

# name = "Raastettua valkokaalia"
# tokens = tokenize_ingredient(name)
# print(tokens)

# HUOM! Yhteinen json sitten meidän kaikkien tokenisoiduille resepteille
with open("recipes_tokenized.json", "w", encoding="utf-8") as f:
    json.dump(
        recipes,
        f,
        ensure_ascii=False,
        indent=2
    )