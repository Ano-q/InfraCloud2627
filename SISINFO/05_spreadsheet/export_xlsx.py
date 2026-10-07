import os
import sys

# Map SISINFO; de andere taakmappen worden toegevoegd zodat hun scripts importeerbaar zijn
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for map_naam in ['01_basisscript', '02_filteren']:
    sys.path.insert(0, os.path.join(ROOT, map_naam))
OUTPUT = os.path.join(ROOT, "output")     # alle gegenereerde bestanden komen hier

from openpyxl import Workbook
from openpyxl.styles import Font
from filter_sysinfo import KOLOMMEN, get_filtered_info

def schrijf_xlsx(pad, rijen, bladnaam="sysinfo"):
    wb = Workbook()                     # een nieuw, leeg Excel-bestand
    ws = wb.active                      # het eerste werkblad
    ws.title = bladnaam

    ws.append(KOLOMMEN)                 # rij 1: de kolomnamen
    for rij in rijen:
        ws.append([rij.get(kolom) for kolom in KOLOMMEN])

    for cel in ws[1]:                   # koprij vet zetten
        cel.font = Font(bold=True)
    ws.freeze_panes = "A2"              # koprij blijft staan bij het scrollen
    for kolom in ws.columns:            # kolombreedte aanpassen aan de inhoud
        breedte = max(len(str(cel.value)) if cel.value is not None else 0 for cel in kolom)
        ws.column_dimensions[kolom[0].column_letter].width = breedte + 2

    wb.save(pad)

if __name__ == "__main__":
    gefilterd = get_filtered_info()
    os.makedirs(OUTPUT, exist_ok=True)
    xlsx_bestand = os.path.join(OUTPUT, f"sysinfo_{gefilterd['computernaam']}.xlsx")
    schrijf_xlsx(xlsx_bestand, [gefilterd])
    print("Bewaard als", xlsx_bestand)
