import libvoikko

voikko = libvoikko.Voikko("fi")

# Testit voikolle, että toimii
# Tehdään myöhemmin sama juttu yhteiselle tokenisoidulle aineistolle

testit = [
    "valkokaalia",
    "sipulia",
    "munia",
    "vehnäjauhoja",
    "paprikaa",
    "suolaa"
]

for sana in testit:
    analyysit = voikko.analyze(sana)

    print(f"Sana: {sana}")
    print(analyysit)
    print()