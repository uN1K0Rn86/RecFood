# import libvoikko

# voikko = libvoikko.Voikko("fi")

# # Testit voikolle, että toimii
# # Tehdään myöhemmin sama juttu yhteiselle tokenisoidulle aineistolle

# testit = [
#     "valkokaalia",
#     "sipulia",
#     "munia",
#     "vehnäjauhoja",
#     "paprikaa",
#     "suolaa"
# ]

# for sana in testit:
#     analyysit = voikko.analyze(sana)

#     print(f"Sana: {sana}")
#     print(analyysit)
#     print()

import libvoikko
import json

voikko = libvoikko.Voikko("fi")

with open("recipes_tokenized.json", "r", encoding="utf-8") as f:
    recipes = json.load(f)

for recipe in recipes:
    for ingredient in recipe["ingredients"]:
        ingredient["lemmatized"] = []

        for token in ingredient["tokens"]:
            analysis = voikko.analyze(token)

            ingredient["lemmatized"].append({
                "token": token,
                "analysis": analysis
            })

with open("recipes_tokenized.json", "w", encoding="utf-8") as f:
    json.dump(
        recipes,
        f,
        ensure_ascii=False,
        indent=2
    )