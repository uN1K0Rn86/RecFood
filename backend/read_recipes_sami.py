import re
import json
from pathlib import Path

path = Path("/home/heinisam/Documents/RecFood/backend/reseptit_sami.txt")

def fix_text(text: str) -> str:
    # normalize common bad replacements from mis-decoding
    replacements = {
        "Ã¤": "ä",
        "Ã¶": "ö",
        "Ã¥": "å",
        "Ã„": "Ä",
        "Ã–": "Ö",
        "Ã…": "Å",
        "–": "-",
        "—": "-",
        "“": '"',
        "”": '"',
        "’": "'",
        "…": "...",
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text

def remove_ocr_hyphens(text: str) -> str:
    # Join words split by a line-break hyphen:
    # "kypsy-\nmistä" -> "kypsymistä"
    text = re.sub(
        r"(?<=[^\W\d_])-\s*\n\s*(?=[^\W\d_])",
        "",
        text,
    )

    # Remove hyphens between letters on the same line
    return re.sub(
        r"(?<=[^\W\d_])-(?=[^\W\d_])",
        "",
        text,
    )

def is_ignored_ingredient_heading(line: str) -> bool:
    return line.casefold() in {
        "täyte",
        "t�yte",
        "kastike",
    }

def fix_ocr_words(text: str) -> str:
    replacements = {
        "lis��m�ll�": "lisäämällä",
        "�rsyyntymist�": "ärsyyntymistä",
        "t�ytel�ist�": "täyteläistä",
        "v�ri�": "väriä",
        "�ljyst�": "öljystä",
        "lis�tt�v�": "lisättävä",
        "lis�t��n": "lisätään",
        "kypsent�misen": "kypsentämisen",
        "selleri�": "selleriä",
        "v�ltt�m�t�n": "välttämätön",
        "l�hemm�ksi": "lähemmäksi",
        "s��nn�llisin": "säännöllisin",
        "v�lein": "välein",
        "pehme��": "pehmeää",
        "lis�tty": "lisätty",
        "kivett�mi�": "kivettömiä",
        "lep��m��n": "lepäämään",
        "j�ljell�": "jäljellä",
        "p�tkittyn�": "pätkittynä",
        "v�kev�ite": "väkevöite",
        "k�ytt�m�st�": "käyttämästä",
        "k��nt�en": "kääntäen",
        "m�rk��n": "märkään",
        "m�rk�": "märkä",
        "k�yt�": "käytä",
        "v�hitellen": "vähitellen",
        "j��htyneen�": "jäähtyneenä",
        "p��llekk�in": "päällekkäin",
        "j��htym��n": "jäähtymään",
        "nestem�ist�": "nestemäistä",
        "ensimm�iseen": "ensimmäiseen",
        "vispil�": "vispilä",
        "j�tt�v�t": "jättävät",
        "pehme�ksi": "pehmeäksi",
        "pehme�": "pehmeä",
        "ymp�ri": "ympäri",
        "revitty�": "revittyä",
        "sirvil�": "sirvilä",
        "sile�lehtist�": "sileälehtistä",
        "l�mpim��n": "lämpimään",
        "l�mpim�n�": "lämpimänä",
        "l�mpim�n": "lämpimän",
        "pehme�t": "pehmeät",
        "leve��": "leveää",
        "kylm��n": "kylmään",
        "kylm��": "kylmää",
        "j�tt��": "jättää",
        "yht�": "yhtä",
        "neli�it�": "neliöitä",
        "siivil�i": "siivilöi",
        "j�lleen": "jälleen",
        "kyps��": "kypsää",
        "kylm�": "kylmä",
        "lis��": "lisää",
        "levylt�": "levyltä",
        "liemest�": "liemestä",
        "ehk�": "ehkä",
        "reik�": "reikä",
        "t�ll�in": "tällöin",
        "r�isky�": "räiskyä",
        "sherry�": "sherryä",
        "l�vikk��n": "lävikköön",
        "j��hty�": "jäähtyä",
        "enemm�n": "enemmän",
        "kevyemm�st�": "kevyemmästä",
        "yrttej�": "yrttejä",
        "reisi�": "reisiä",
        "siipi�": "siipiä",
        "fileet�": "fileetä",
        "siirr�": "siirrä",
        "m��ri�": "määriä",
        "m��r�inen": "määräinen",
        "viini�": "viiniä",
        "v�kev��": "väkevää",
        "j�tti": "jätti",
        "lis�t�": "lisätä",
        "l�mm�lle": "lämmölle",
        "lient�": "lientä",
        "h�mment�en": "hämmentäen",
        "inkiv��ri�": "inkivääriä",
        "inkiv��ri": "inkivääri",
        "mink�": "minkä",
        "s�ilyy": "säilyy",
        "peitt��": "peittää",
        "pient�": "pientä",
        "hyv�ns�": "hyvänsä",
        "peitettyn�": "peitettynä",
        "tehd�": "tehdä",
        "j�t�": "jätä",
        "pyrst�t": "pyrstöt",
        "t�ss�": "tässä",
        "pist�": "pistä",
        "leip�": "leipä",
        "leiv�n": "leivän",
        "s�mpyl�iden": "sämpylöiden",
        "levitt�m�ll�": "levittämällä",
        "heit�": "heitä",
        "�ljy�": "öljyä",
        "�ljy": "öljy",
        "tilli�": "tilliä",
        "h�nn�n": "hännän",
        "ett�": "että",
        "v�ri": "väri",
        "v�li": "väli",
        "t�m�": "tämä",
        "peit�": "peitä",
        "t�ytyy": "täytyy",
        "l�pi": "läpi",
        "p�tkiksi": "pätkiksi",
        "l�mm�ll�": "lämmöllä",
        "l�ht�isin": "lähtöisin",
        "tiivist��": "tiivistää",
        "pitemm�n": "pitemmän",
        "hyv�": "hyvä",
        "s�ilyt�": "säilytä",
        "perint��": "perintöä",
        "liedelt�": "liedeltä",
        "p��ll�": "päällä",
        "k�teen": "käteen",
        "pitki�": "pitkiä",
        "leivit�": "leivitä",
        "s�ilytt��": "säilyttää",
        "SIS�LT�": "SISÄLTÖ",
        "p�hkin�": "pähkinä",
        "vehn�": "vehnä",
        "kypsi�": "kypsiä",
        "etel�": "etelä",
        "keit�": "keitä",
        "sek�": "sekä",
        "t�yte": "täyte",
        "pid�": "pidä",
        "y�n": "yön",
        "yl�s": "ylös",
        "l�hes": "lähes",
        "kes�": "kesä",
        "l�mp��": "lämpöä",
        "l�mpi": "lämpi",
        "vihre�": "vihreä",
        "ziti�": "zitiä",
        "Pienenn�": "Pienennä",
        "penne�": "penneä",
        "h�nt��": "häntää",
        "�yri�is": "äyriäis",
        "h�yry": "höyry",
        "h�nt�": "häntä",
        "t�t�": "tätä",
        "siemeni�": "siemeniä",
        "siemenisi�": "siemenisiä",
        "sieni�": "sieniä",
        "pyreet�": "pyreetä",
        "fileit�": "fileitä",
        "kiinte�": "kiinteä",
        "lehti�": "lehtiä",
        "Mit�": "Mitä",
        "mik�": "mikä",
        "ved�": "vedä",
        "syv�": "syvä",
        "est��": "estää",
        "p��n": "pään",
        "t��n": "tään",
        "sit�": "sitä",
        "lis�": "lisä",
        "siit�": "siitä",
        "h�rk�": "härkä",
        "l�mmi": "lämmi",
        "my�s": "myös",
        "t�isist�": "täisistä",
        "kyntt�": "kynttä",
        "h�mmen": "hämmen",
        "k��nn": "käänn",
        "mist�": "mistä",
        "nein�": "neinä",
        "lehte�": "lehteä",
        "kyps�": "kypsä",
        "h�r�n": "härän",
        "viel�": "vielä",
        "selk�": "selkä",
        "kev�t": "kevät",
        "n��n": "nään",
        "list�": "listä",
        "l�mp�": "lämpö",
        "v�h�": "vähä",
        "tyin�": "tyinä",
        "p�in": "päin",
        "tyj�": "tyjä",
        "keitt��": "keittää",
        "keitt�": "keittä",
        "p��": "pää",
        "j��": "jää",
        "ll�": "llä",
        "k�y": "käy",
        "mm�n": "mmän",
        "m�ll�": "mällä",
        "v�t": "vät",
        "�l�": "älä",
        "tt��": "ttää",
        "nn�": "nnä",
        "ss�": "ssä",
        "v��": "vää",
        "ni�": "niä",
        "tt�": "ttä",
        "eit�": "eitä",
        "lt�": "ltä"
    }

    for bad, good in replacements.items():
        text = re.sub(re.escape(bad), good, text, flags=re.IGNORECASE)

    return text

def parse_number(value: str):
    value = value.strip().replace(",", ".")
    value = value.replace("I", "1").replace("l", "1")
    value = value.replace("½", "1/2").replace("¼", "1/4").replace("¾", "3/4")

    if not value:
        return None

    if re.fullmatch(r"\d+\s+\d+/\d+", value):
        whole, frac = value.split()
        n, d = frac.split("/")
        return float(whole) + (float(n) / float(d))

    if re.fullmatch(r"\d+/\d+", value):
        n, d = value.split("/")
        return float(n) / float(d)

    if re.fullmatch(r"\d+", value):
        return float(value)

    return None

def is_recipe_title(line: str) -> bool:
    if not line or len(line) < 3:
        return False

    # ignore metadata lines
    if line.startswith(("Valmistelut:", "Kypsennys:", "YHDEN ANNOKSEN", "HUOM", "LISUKKEEKSI")):
        return False

    # titles are uppercase-ish names like "PRIMAVERA", "POMODORO", "SPAGHETTI BOLOGNESE"
    return bool(re.fullmatch(
        r"[A-ZÅÄÖ0-9 ,./()'\-/]+",
        line,
    ))

def parse_ingredient(line: str):
    line = line.strip().lstrip("|").strip()

    if not line or line in {"*", "**", "***"}:
        return None

    # OCR commonly reads "I" or "l" instead of "1" at the beginning.
    line = re.sub(r"^[Il]\b", "1", line)

    pattern = re.compile(
        r"^(?P<amount>"
        r"(?:\d+\s+\d+/\d+|\d+/\d+|\d+(?:[.,]\d+)?)"
        r")?\s*"
        r"(?P<unit>kg|mg|g|dl|ml|l|tl|rkl|kpl|pala|rivi|"
        r"viipaletta|viipaleita|kynsi|kananmuna|munaa|rki|ti|di)?\s*"
        r"(?=\s|$)\s*"
        r"(?:\((?P<alt_amount>[\d\s/.,]+)\s*"
        r"(?P<alt_unit>kg|mg|g|dl|ml|l)\))?\s*"
        r"(?P<name>.+)$",
        re.IGNORECASE,
    )

    match = pattern.match(line)

    if not match:
        return {
            "amount": None,
            "unit": None,
            "name": line,
        }

    amount = match.group("amount") or match.group("alt_amount")
    unit = match.group("unit") or match.group("alt_unit") or ""
    unit = unit.lower().replace("rki", "rkl")
    unit = unit.lower().replace("ti", "tl")
    unit = unit.lower().replace("di", "dl")
    name = match.group("name").strip()

    return {
        "amount": parse_number(amount) if amount else None,
        "unit": unit,
        "name": name,
    }


def is_instruction_line(line: str) -> bool:
    line = line.lstrip("|").strip()

    # OCR may read the instruction's first character as "I" or "l".
    line = re.sub(r"^[Il]\s+(?=Kuumenna|Lisää|Lisaa|Sekoita|"
                  r"Mausta|Tarjoa|Paloittele|Pilko|Leikkaa|Sulata|"
                  r"Nosta|Ota|Pane|Kaada|Valuta|Anna|Poista|"
                  r"Jaa|Valmista|Tee|Aseta|Kypsennä|Paista|"
                  r"Sido|Peitä|Pistä)\b", "", line, flags=re.IGNORECASE)

    return bool(re.match(
        r"^\d+\s+(Keitä|Kuumenna|Lisää|Lisaa|Sekoita|Mausta|Tarjoa|"
        r"Paloittele|Pilko|Leikkaa|Sulata|Nosta|Ota|Pane|Kaada|Valuta|Anna|"
        r"Poista|Jaa|Valmista|Tee|Aseta|Kypsennä|Paista|Sido|Peitä|Pistä|tai)\b",
        line,
        re.IGNORECASE,
    )) or bool(re.match(
        r"^(Keitä|Kuumenna|Lisää|Lisaa|Sekoita|Mausta|Tarjoa|"
        r"Paloittele|Pilko|Leikkaa|Sulata|Nosta|Ota|Pane|Kaada|Valuta|Anna|"
        r"Poista|Jaa|Valmista|Tee|Aseta|Kypsennä|Paista|Sido|Peitä|Pistä)\b",
        line,
        re.IGNORECASE,
    ))

def parse_nutrition(raw: str):
    out = {}
    pairs = re.findall(r"(\d+(?:\.\d+)?)\s*(g|mg|kJ|kcal)\s*([a-zäöåA-ZÄÖÅ]+)", raw, re.I)

    for value, unit, label in pairs:
        label = label.lower()
        value = float(value)

        if "proteiini" in label:
            out["protein_g"] = value
        elif "rasva" in label:
            out["fat_g"] = value
        elif "hiilihydraatte" in label:
            out["carbohydrates_g"] = value
        elif "ravintokuitu" in label:
            out["fiber_g"] = value
        elif "kolesterol" in label:
            out["cholesterol_mg"] = value
        elif "kcal" in label:
            out["energy_kcal"] = value

    return out

recipes = []
current = None
state = "idle"

try:
    text = path.read_text(encoding="utf-8")
except UnicodeDecodeError:
    text = path.read_text(encoding="cp1252")

text = fix_text(text)
text = remove_ocr_hyphens(text)
text = fix_ocr_words(text)

lines = text.splitlines()

for raw in lines:
    line = raw.strip()
    if not line:
        continue

    if is_recipe_title(line):
        if current:
            recipes.append(current)
        current = {
            "name": line,
            "preparation_time": "",
            "cooking_time": "",
            "servings": "",
            "ingredients": [],
            "instructions": [],
            "nutrition": {}
        }
        state = "meta"
        continue

    if not current:
        continue

    if line.startswith("Valmistelut:"):
        current["preparation_time"] = line.split(":", 1)[1].strip()
        state = "meta"
        continue

    if line.startswith("Kypsennys:"):
        current["cooking_time"] = line.split(":", 1)[1].strip()
        state = "meta"
        continue

    if re.match(r"^\d+\s*-\s*\d+\s*annosta|\d+\s*annosta", line, re.I):
        current["servings"] = line
        state = "ingredients"
        continue

    if "YHDEN ANNOKSEN" in line or "RAVINTOSIS" in line.upper():
        current["nutrition_raw"] = line
        state = "nutrition"
        continue

    if state == "ingredients":
        if is_ignored_ingredient_heading(line):
            continue

        if is_instruction_line(line):
            state = "instructions"

            line = line.lstrip("|").strip()
            if re.match(r"^\d+\s+", line):
                line = re.sub(r"^\d+\s*", "", line)

            current["instructions"].append(line)
            continue

        # Ignore visual separators from the scanned document.
        if line in {"*", "**", "***"}:
            continue

        ingredient = parse_ingredient(line)

        if ingredient and ingredient["name"]:
            current["ingredients"].append(ingredient)

        continue

    if state == "instructions":
        if "YHDEN ANNOKSEN" in line or "RAVINTOSIS" in line.upper():
            state = "nutrition"
            current["nutrition_raw"] = line
            continue

        line = line.lstrip("|").strip()
        if re.match(r"^\d+\s+", line):
            line = re.sub(r"^\d+\s*", "", line)

        if line:
            current["instructions"].append(line)
        continue

    if state == "nutrition":
        current["nutrition_raw"] = current.get("nutrition_raw", "") + " " + line

if current:
    recipes.append(current)

# final pass for nutrition
for recipe in recipes:
    raw_nutrition = recipe.get("nutrition_raw", "")
    recipe["nutrition"] = parse_nutrition(raw_nutrition)
    recipe.pop("nutrition_raw", None)

# save as JSON
with open("/home/heinisam/Documents/RecFood/backend/recipes_sami.json", "w", encoding="utf-8") as f:
    json.dump(recipes, f, ensure_ascii=False, indent=2)

print(f"Parsed {len(recipes)} recipes.")
print(json.dumps(recipes[0], ensure_ascii=False, indent=2)[:1000])