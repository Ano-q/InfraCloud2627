import os
import sys

# Map SISINFO; de andere taakmappen worden toegevoegd zodat hun scripts importeerbaar zijn
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for map_naam in ['01_basisscript', '02_filteren', '04_csv', '06_samenvoegen']:
    sys.path.insert(0, os.path.join(ROOT, map_naam))

import re
import ipaddress
from filter_sysinfo import get_filtered_info
from export_csv import lees_csv
from merge_team_csv import TEAM_CSV

MAC_PATROON = re.compile(r"^([0-9A-F]{2}:){5}[0-9A-F]{2}$")
VERPLICHT = ["computernaam", "processor", "ram_gb", "opslag_gb", "mac", "ipv4"]

def valideer_rij(rij):
    # Geeft een lijst met gevonden problemen terug (lege lijst = alles in orde).
    problemen = []

    for kolom in VERPLICHT:
        if not rij.get(kolom):
            problemen.append(f"{kolom} is leeg")

    if rij.get("mac") and not MAC_PATROON.match(rij["mac"]):
        problemen.append(f"mac heeft een ongeldige vorm: {rij['mac']}")

    for kolom, versie in [("ipv4", 4), ("ipv6", 6), ("ipv6_linklocal", 6)]:
        waarde = rij.get(kolom)
        if not waarde:
            continue
        try:
            adres = ipaddress.ip_address(waarde)
            if adres.version != versie:
                problemen.append(f"{kolom} is geen IPv{versie}-adres: {waarde}")
            if kolom == "ipv6_linklocal" and not adres.is_link_local:
                problemen.append(f"{kolom} is geen link-local adres: {waarde}")
            if kolom == "ipv4" and (adres.is_loopback or adres.is_link_local):
                problemen.append(f"{kolom} is geen bruikbaar adres: {waarde}")
        except ValueError:
            problemen.append(f"{kolom} is geen geldig IP-adres: {waarde}")

    for kolom, minimum in [("ram_gb", 0.5), ("opslag_gb", 1), ("cpu_cores", 1)]:
        waarde = rij.get(kolom)
        if not waarde:
            continue
        try:
            if float(waarde) < minimum:
                problemen.append(f"{kolom} is onwaarschijnlijk klein: {waarde}")
        except ValueError:
            problemen.append(f"{kolom} is geen getal: {waarde}")

    return problemen

if __name__ == "__main__":
    # 1. Elke rij van het teambestand controleren
    team_rijen = lees_csv(TEAM_CSV)
    for rij in team_rijen:
        problemen = valideer_rij(rij)
        print(rij["computernaam"], "->", "OK" if not problemen else problemen)

    # 2. Dubbele computernamen
    namen = [rij["computernaam"] for rij in team_rijen]
    dubbels = {naam for naam in namen if namen.count(naam) > 1}
    print("Dubbele computernamen:", dubbels if dubbels else "geen")

    # 2b. Dubbele serienummers (zelfde hardware twee keer in de lijst)
    serials = [rij["serienummer"] for rij in team_rijen if rij["serienummer"]]
    dubbele_serials = {s for s in serials if serials.count(s) > 1}
    print("Dubbele serienummers:", dubbele_serials if dubbele_serials else "geen")

    # 3. De eigen computer vergelijken met een nieuwe meting
    nu = get_filtered_info()
    for rij in team_rijen:
        if rij["computernaam"] == nu["computernaam"]:
            for kolom in ["computernaam", "serienummer", "ram_gb", "processor", "ipv4", "mac", "opslag_gb"]:
                zelfde = str(rij[kolom]) == str(nu[kolom] if nu[kolom] is not None else "")
                print(f"  {kolom:13} bestand: {rij[kolom]:40} nu: {nu[kolom]}  {'OK' if zelfde else 'VERSCHIL'}")
