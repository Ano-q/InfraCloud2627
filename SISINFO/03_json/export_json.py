import os
import sys

# Map SISINFO; de andere taakmappen worden toegevoegd zodat hun scripts importeerbaar zijn
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for map_naam in ['01_basisscript', '02_filteren']:
    sys.path.insert(0, os.path.join(ROOT, map_naam))
OUTPUT = os.path.join(ROOT, "output")     # alle gegenereerde bestanden komen hier

import json
from filter_sysinfo import get_filtered_info

if __name__ == "__main__":
    gefilterd = get_filtered_info()
    os.makedirs(OUTPUT, exist_ok=True)
    json_bestand = os.path.join(OUTPUT, f"sysinfo_{gefilterd['computernaam']}.json")

    # 1. dict -> JSON-bestand
    with open(json_bestand, "w", encoding="utf-8") as f:
        json.dump(gefilterd, f, indent=2)
    print("Bewaard als", json_bestand)

    # 2. JSON-bestand -> dict
    with open(json_bestand, "r", encoding="utf-8") as f:
        ingelezen = json.load(f)
    print("Type na inlezen:", type(ingelezen))

    # 3. Controleren of alles overeenkomt
    print("Volledig gelijk aan het origineel:", ingelezen == gefilterd)
    for sleutel in ["computernaam", "ram_gb", "processor", "ipv4", "mac", "opslag_gb"]:
        zelfde = ingelezen[sleutel] == gefilterd[sleutel]
        print(f"{sleutel:15} {str(ingelezen[sleutel]):45} {'OK' if zelfde else 'VERSCHIL'}")
