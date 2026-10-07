import os
import sys

# Map SISINFO; de andere taakmappen worden toegevoegd zodat hun scripts importeerbaar zijn
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for map_naam in ['01_basisscript', '02_filteren', '04_csv']:
    sys.path.insert(0, os.path.join(ROOT, map_naam))
OUTPUT = os.path.join(ROOT, "output")     # alle gegenereerde bestanden komen hier

import glob
from filter_sysinfo import KOLOMMEN
from export_csv import CSV_MAP, schrijf_csv, lees_csv

TEAM_CSV = os.path.join(OUTPUT, "team_sysinfo.csv")

def voeg_samen(map_met_csv):
    per_computer = {}
    bestanden = sorted(glob.glob(os.path.join(map_met_csv, "sysinfo_*.csv")))
    for pad in bestanden:
        rijen = lees_csv(pad)
        print(f"Ingelezen: {pad} ({len(rijen)} rij(en))")
        for rij in rijen:
            ontbreekt = [k for k in KOLOMMEN if k not in rij]
            if ontbreekt:
                print("   let op, ontbrekende kolommen:", ontbreekt)
            # Elke rij in de afgesproken structuur gieten; wat ontbreekt wordt leeg.
            nette_rij = {k: (rij.get(k) or "") for k in KOLOMMEN}
            sleutel = nette_rij["serienummer"] or nette_rij["computernaam"] or pad
            per_computer[sleutel] = nette_rij
    return list(per_computer.values())

if __name__ == "__main__":
    team = voeg_samen(CSV_MAP)
    schrijf_csv(TEAM_CSV, team)
    print(f"\n{len(team)} computer(s) samengevoegd in {TEAM_CSV}")
    for rij in team:
        print("  ", rij["computernaam"], "|", rij["processor"], "|", rij["ram_gb"], "GB RAM")
