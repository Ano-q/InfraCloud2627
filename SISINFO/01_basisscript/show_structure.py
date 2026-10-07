import os
import sys

# Map SISINFO; de andere taakmappen worden toegevoegd zodat hun scripts importeerbaar zijn
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for map_naam in ['01_basisscript']:
    sys.path.insert(0, os.path.join(ROOT, map_naam))

from collect_sysinfo import collect_system_info

if __name__ == "__main__":
    info = collect_system_info()
    print("Bovenste laag :", list(info.keys()))
    print("cpu           :", list(info["cpu"].keys()))
    print("memory        :", list(info["memory"].keys()))
    print("storage       :", list(info["storage"].keys()))
    print("network       :", list(info["network"].keys()))
    print("interfaces    :", list(info["network"]["interfaces"].keys()))
