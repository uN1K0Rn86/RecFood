import re
import json
from pathlib import Path

INPUT_FILE = "recipes.txt"
OUTPUT_FILE = "recipes.json"

# APUTOIMINNOT

def clean(line):
    #Siivoaa rivin alusta ja lopusta ylimääräiset välilyönnit
    return line.strip()


def is_numbered_instruction(line):
    return bool(re.match(r"^\d+\.\s+", line))

# AINESOSIEN TUNNISTAMINEN

# Tavallisimmat yksiköt.
# Mukana myös joitakin lähdemateriaalissa esiintyviä muotoja.
UNITS = [
    "kg",
    "mg",
    "ml",
    "cl",
    "dl",
    "del",
    "rkl",
    "tl",
    "pkt",
    "tlk",
    "rs",
    "kpl",
    "ps",
    "pussi",
    "pussia",
    "purkki",
    "purkkia",
    "rasia",
    "rasiaa",
    "nippu",
    "l",
    "g",
]


# Unicode-murtoluvut
UNICODE_FRACTIONS = "½⅓⅔¼¾⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞"

# Tavallinen luku, desimaali, murtoluku, sekamurtoluku,
# määräväli tai lähdemateriaalin kaltainen "1/½".
AMOUNT_PATTERN = (
    r"(?:"
    # Määräväli: 3-4 tai 3–4
    r"\d+(?:[.,]\d+)?\s*[-–]\s*\d+(?:[.,]\d+)?"
    r"|"
    # Sekamurtoluku: 1 1/2
    r"\d+\s+\d+/\d+"
    r"|"
    # Tavallinen murtoluku: 1/2
    r"\d+/\d+"
    r"|"
    # Esim. 1/½
    r"\d+/\s*" + f"[{UNICODE_FRACTIONS}]" + r"?"
    r"|"
    # Desimaali tai kokonaisluku
    r"\d+(?:[.,]\d+)?"
    r"|"
    # Unicode-murtoluku
    r"[" + UNICODE_FRACTIONS + r"]"
    r")"
)

# Yksikkö, jonka jälkeen pitää olla sana-/sisältöä.
UNIT_PATTERN = "|".join(
    sorted((re.escape(u) for u in UNITS), key=len, reverse=True)
)

AMOUNT_WITH_OPTIONAL_UNIT_RE = re.compile(
    rf"^\(?\s*"
    rf"(?P<amount>{AMOUNT_PATTERN})"
    rf"\s*"
    rf"(?P<unit>{UNIT_PATTERN})?"
    rf"\s*"
    rf"\)?"
    rf"\s+"
    rf"(?P<name>.+?)"
    rf"\s*$",
    re.IGNORECASE,
)

# MÄÄRÄTTÖMIEN AINESOSIEN TUNNISTAMINEN

# Näillä sanoilla alkavat rivit ovat yleensä ainesosia,
# vaikka niissä ei olisi määrää.
UNAMOUNTED_INGREDIENT_STARTS = [
    "kourallinen ",
    "tilkka ",
    "ripaus ",
    "pieni ripaus ",
    "öljyä",
    "öljyä/voita",
    "voita ",
    "currya ",
    "limeä",
    "lehtipersiljaa",
    "mausteita",
    "karkeaa suolaa",
    "suolaa & pippuria",
    "suolaa ja pippuria",
    "reilu",
    "valkosipulinkynsi",
    "valkosipulinkynttä",
    "valkosipulinkynsiä",
    "kasvislientä",
]


def is_unamounted_ingredient(line):
    """Tunnistaa ainesosan, jolla ei ole numeroalkuista määrää."""
    low = line.lower().strip()

    for start in UNAMOUNTED_INGREDIENT_STARTS:
        if low.startswith(start):
            return True

    return False


def is_ingredient(line):
    #Tunnistaa ainesosarivin
  
    line = clean(line)

    if not line:
        return False

    # Numeroitu rivi ei ole ainesosa.
    if is_numbered_instruction(line):
        return False

    # Sulkeisiin pakattu määrä, esim.
    # (½ dl kuivattuja hedelmiä)
    if re.match(
        rf"^\(\s*{AMOUNT_PATTERN}(?:\s*{UNIT_PATTERN})?\s+",
        line,
        re.IGNORECASE,
    ):
        return True

    # Määrä + mahdollinen yksikkö.
    #
    # Tärkeää:
    # sallitaan sekä
    #   100 g voita
    # että
    #   100g voita
    #
    # sekä esimerkiksi
    #   1-2 valkosipulinkynttä
    #   1-2 tl sambal oelekia
    #   ½ tl suolaa
    #   2,5 dl vettä
    if re.match(
        rf"^\s*{AMOUNT_PATTERN}\s*-?\s*(?:{UNIT_PATTERN})?\s+.+$",
        line,
        re.IGNORECASE,
    ):
        return True

    # Määrätön ainesosa
    if is_unamounted_ingredient(line):
        return True

    if re.match(
        rf"^\s*{AMOUNT_PATTERN}\s+\w+",
        line,
        re.IGNORECASE,
    ):
        return True

    return False

# AINESOSARYHMIEN OTSIKOT

# Näitä EI pidä tulkita uusiksi resepteiksi.

SECTION_HEADINGS = {
    "pohja",
    "täyte",
    "täytteet",
    "kastike",
    "jogurttikastike",
    "salaatti",
    "lisuke",
    "kuorrutus",
    "korppujauhoseos",
    "marinadi",
}


def is_section_heading(line):
    """
    Tunnistaa ainesosaryhmän otsikon.

    Esimerkiksi:
        Pohja:
        Täyte:
        Jogurttikastike

    Kaksoispiste tekee tunnistuksesta varman.
    Lisäksi tunnetut ryhmäotsikot tunnistetaan ilman kaksoispistettä.
    """

    line = clean(line)

    if not line:
        return False

    low = line.lower().rstrip(":")

    if low in SECTION_HEADINGS:
        return True

    # Esim. "Pohja:" / "Täyte:"
    if line.endswith(":"):
        # Varmistetaan, ettei tämä ole esimerkiksi kokonainen lause.
        if len(line.split()) <= 4:
            return True

    return False

# OHJEIDEN TUNNISTAMINEN

INSTRUCTION_STARTS = [
    "kuumenna ",
    "kumoa ",
    "lisää ",
    "mausta ",
    "sekoita ",
    "mittaa ",
    "vatkaa ",
    "paista ",
    "keitä ",
    "hauduta ",
    "nosta ",
    "kaada ",
    "pursota ",
    "anna ",
    "leikkaa ",
    "huuhtele ",
    "muotoile ",
    "siirrä ",
    "tarjoile ",
    "sulata ",
    "halkaise ",
    "ripottele ",
    "kuori ",
    "pilko ",
    "silppua ",
    "lämmitä ",
    "hienonna ",
    "puhdista ",
    "soseuta ",
    "voitele ",
    "pyörittele ",
    "kääntele ",
    "painele ",
    "kauli ",
    "levitä ",
    "kiehauta ",
    "kypsennä ",
    "tarkista ",
    "murskaa ",
    "sekoita",
    "lisää",
    "mausta",
    "kuumenna",
    "kumoa",
    "keitä",
    "paista",
]


def is_instruction(line):
    """
    Tunnistaa numeroimattoman ohjerivin.
    """
    line = clean(line)

    if not line:
        return False

    if is_numbered_instruction(line):
        return True

    low = line.lower()

    return any(low.startswith(start) for start in INSTRUCTION_STARTS)


# AINESOSAN PARSINTA

def parse_ingredient(line):
    """
    Muuttaa esimerkiksi:

        5 g suolaa
        1-2 valkosipulinkynttä
        ½ tl chilijauhetta
        1 1/2 rkl öljyä
        Kourallinen oliiveja

    muotoon:

        {
            "amount": "5",
            "unit": "g",
            "name": "suolaa"
        }
    """

    line = clean(line)

    # Poistetaan ympäröivät sulut vain siinä tapauksessa,
    # että koko rivi on valinnainen ainesosa:
    # (½ dl kuivattuja hedelmiä)
    optional = False

    if line.startswith("(") and line.endswith(")"):
        inner = line[1:-1].strip()

        if re.match(
            rf"^{AMOUNT_PATTERN}(?:\s|$)",
            inner,
            re.IGNORECASE,
        ):
            line = inner
            optional = True

    match = AMOUNT_WITH_OPTIONAL_UNIT_RE.match(line)

    if match:
        amount = match.group("amount").strip()
        unit = (match.group("unit") or "").strip()
        name = match.group("name").strip()

        result = {
            "amount": amount,
            "unit": unit,
            "name": name,
        }

        return result

    # Jos rivillä on numero mutta yllä oleva regex ei saanut sitä
    # jostain syystä parsittua, pidetään koko rivi ainesosan nimenä.
    return {
        "amount": "",
        "unit": "",
        "name": line,
    }


# RESEPTIN OTSIKKO

def parse_title(line):
    """
    Esimerkiksi:

        Kikhernepyörykät (n. 4 annosta)

    ->

        name = Kikhernepyörykät
        servings = n. 4 annosta

    Myös esimerkiksi:
        Churros (20 kpl)
        Keitto (4 annosta)
        Intialainen linssicurry (n. 2:lle)
    """

    line = clean(line)

    # Etsitään viimeinen sulkeissa oleva osa.
    match = re.match(r"^(.*?)\s*\(([^()]*)\)\s*$", line)

    if match:
        name = match.group(1).strip()
        possible_servings = match.group(2).strip()

        low = possible_servings.lower()

        # Tyypillisiä tarjoilumäärän merkintöjä.
        if (
            "annos" in low
            or "kpl" in low
            or ":lle" in low
            or "hlö" in low
            or "henkilö" in low
        ):
            return name, possible_servings

    return line, None


# SEURAAVAN MERKITYKSELLISEN RIVIN HAKU

def next_nonempty_index(lines, start):
    #Palauttaa seuraavan ei-tyhjän rivin indeksin
    i = start

    while i < len(lines):
        if clean(lines[i]):
            return i
        i += 1

    return None


# RESEPTIEN ALKUJEN ETSIMINEN

def looks_like_recipe_title(lines, index):
    """
    Päättelee, voiko rivi olla uuden reseptin otsikko.

    Tärkeä ero esimerkiksi:

        Jogurttikastike
        2 dl jogurttia

    vs.

        Raparperihilloke
        Tilkka vettä

    Molemmat näyttävät päällepäin otsikoilta.

    Tunnettu ainesosaryhmä kuten Jogurttikastike suljetaan pois,
    mutta Raparperihilloke voidaan tunnistaa uudeksi reseptiksi,
    koska sen jälkeen alkaa uusi ainesosalista.
    """

    line = clean(lines[index])

    if not line:
        return False

    if is_numbered_instruction(line):
        return False

    if is_ingredient(line):
        return False

    if is_section_heading(line):
        return False

    # Seuraava ei-tyhjä rivi.
    next_i = next_nonempty_index(lines, index + 1)

    if next_i is None:
        return False

    next_line = clean(lines[next_i])

    # Jos seuraavana on suoraan ainesosa,
    # tämä on vahva merkki reseptin otsikosta.
    if is_ingredient(next_line):
        return True

    # Jos seuraavana on ryhmäotsikko, katsotaan sen jälkeistä riviä.
    if is_section_heading(next_line):
        after_section = next_nonempty_index(lines, next_i + 1)

        if after_section is not None:
            if is_ingredient(clean(lines[after_section])):
                return True

    return False


def find_recipe_starts(lines):
    """
    Etsii kaikkien reseptien alut.

    Esimerkiksi:

        Kurpitsakeitto
        800 g kurpitsaa
        ...
        1. Kuori...

        Raparperihilloke
        Tilkka vettä
        3 dl sokeria
        ...

    tuottaa indeksit molempiin resepteihin.
    """

    starts = []

    for i, raw_line in enumerate(lines):
        line = clean(raw_line)

        if not line:
            continue

        if looks_like_recipe_title(lines, i):
            starts.append(i)

    return starts


# YKSITTÄISEN RESEPTIN PARSINTA

def parse_recipe(lines, start, end):
    """
    Parsii yhden reseptin.

    Aluksi oletetaan, että ollaan ainesosissa.
    Kun ensimmäinen ohje tulee vastaan, siirrytään ohjetilaan.
    """

    title_line = clean(lines[start])
    name, servings = parse_title(title_line)

    recipe = {
        "name": name,
    }

    if servings:
        recipe["servings"] = servings

    ingredients = []
    instructions = []

    mode = "ingredients"

    i = start + 1

    while i < end:
        line = clean(lines[i])

        if not line:
            i += 1
            continue

        # Ainesosaryhmän otsikko -> ohitetaan.
        if is_section_heading(line):
            i += 1
            continue

        # Numeroitu ohje -> varmasti ohjeisiin.
        if is_numbered_instruction(line):
            mode = "instructions"
            instructions.append(line)
            i += 1
            continue

        # Selvästi tunnistettava ohje.
        if is_instruction(line):
            mode = "instructions"
            instructions.append(line)
            i += 1
            continue

        # Jos ollaan ainesosavaiheessa, kaikki ainesosat otetaan mukaan.
        if mode == "ingredients":
            if is_ingredient(line):
                ingredients.append(parse_ingredient(line))
            else:
                # Tuntematon rivi ainesosavaiheessa:
                # mieluummin säilytetään se ainesosana kuin hukataan.
                ingredients.append({
                    "amount": "",
                    "unit": "",
                    "name": line,
                })

            i += 1
            continue

        # Ohjevaiheessa kaikki muut rivit kuuluvat ohjeeseen.
        instructions.append(line)

        i += 1

    recipe["ingredients"] = ingredients

    if instructions:
        recipe["instructions"] = instructions

    return recipe


# PÄÄOHJELMA

def main():
    input_path = Path(INPUT_FILE)
    output_path = Path(OUTPUT_FILE)

    if not input_path.exists():
        print(f"VIRHE: tiedostoa ei löydy: {INPUT_FILE}")
        return

    text = input_path.read_text(encoding="utf-8")

    # Word Online -kopioinnissa voi tulla \r-rivejä.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    lines = text.split("\n")

    print(f"Luetaan: {INPUT_FILE}")
    print(f"Rivejä: {len(lines)}")

    starts = find_recipe_starts(lines)

    print(f"Löydettiin reseptien alkuja: {len(starts)}")

    if not starts:
        print("VAROITUS: yhtään reseptiä ei tunnistettu.")
        return

    recipes = []

    for position, start in enumerate(starts):
        if position + 1 < len(starts):
            end = starts[position + 1]
        else:
            end = len(lines)

        recipe = parse_recipe(lines, start, end)

        recipes.append(recipe)

    # Kirjoitetaan JSON UTF-8-muodossa.
    output_path.write_text(
        json.dumps(
            recipes,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Valmis: {OUTPUT_FILE}")
    print(f"Reseptejä: {len(recipes)}")


if __name__ == "__main__":
    main()