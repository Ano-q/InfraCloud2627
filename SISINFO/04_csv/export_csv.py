import os
import sys

# Map SISINFO; de andere taakmappen worden toegevoegd zodat hun scripts importeerbaar zijn
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for map_naam in ['01_basisscript', '02_filteren']:
    sys.path.insert(0, os.path.join(ROOT, map_naam))
OUTPUT = os.path.join(ROOT, "output")     # alle gegenereerde bestanden komen hier

import csv
from filter_sysinfo import KOLOMMEN, get_filtered_info

CSV_MAP = os.path.join(OUTPUT, "team_csv")
SCHEIDINGSTEKEN = ";"

def schrijf_csv(pad, rijen):
    # Schrijft een lijst van dicts naar een CSV-bestand met de afgesproken kolommen.
    with open(pad, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=KOLOMMEN, delimiter=SCHEIDINGSTEKEN,
                                restval="", extrasaction="ignore")
        writer.writeheader()            # de rij met kolomnamen
        writer.writerows(rijen)         # de gegevens

def lees_csv(pad):
    # Leest een CSV-bestand en geeft een lijst van dicts terug (één dict per rij).
    with open(pad, "r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f, delimiter=SCHEIDINGSTEKEN))

if __name__ == "__main__":
    os.makedirs(CSV_MAP, exist_ok=True)     # maakt de map als ze nog niet bestaat
    gefilterd = get_filtered_info()
    csv_bestand = os.path.join(CSV_MAP, f"sysinfo_{gefilterd['computernaam']}.csv")
    schrijf_csv(csv_bestand, [gefilterd])
    print("Bewaard als", csv_bestand)

    # Opnieuw inlezen om te tonen dat het werkt
    print(lees_csv(csv_bestand))
