import os
import sys

# Map SISINFO; de andere taakmappen worden toegevoegd zodat hun scripts importeerbaar zijn
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for map_naam in ['01_basisscript']:
    sys.path.insert(0, os.path.join(ROOT, map_naam))

import os
import platform
import socket
import psutil

from collect_sysinfo import collect_system_info
from system_details import add_system_details
from primary_interface import find_primary_interface

KOLOMMEN = [
    "computernaam", "computermodel", "serienummer", "processor", "cpu_cores", "cpu_max_mhz",
    "ram_gb", "fs_type", "opslag_gb", "mac", "ipv4", "ipv6", "ipv6_linklocal",
]

def to_gb(aantal_bytes):
    return round(aantal_bytes / 1024**3, 1)

def get_system_partition(info):
    storage = info["storage"]
    if platform.system() == "Windows":
        gezocht = os.environ.get("SystemDrive", "C:") + "\\"
    else:
        gezocht = "/"
    if gezocht in storage:
        return storage[gezocht]
    # Reserve: de grootste partitie
    if storage:
        return max(storage.values(), key=lambda p: p["total"])
    return None

def filter_system_info(info):
    # Begin met alle kolommen op None; wat we vinden vullen we in.
    result = dict.fromkeys(KOLOMMEN)

    result["computernaam"] = info["network"]["hostname"]
    result["computermodel"] = info["system"]["model"]
    result["serienummer"] = info["system"]["serial"]
    result["processor"] = info["system"]["cpu_name"]
    result["cpu_cores"] = info["cpu"]["physical_cores"]

    freq = info["cpu"]["cpu_freq"]
    if freq and freq["max"]:
        result["cpu_max_mhz"] = round(freq["max"])

    result["ram_gb"] = to_gb(info["memory"]["total"])

    partitie = get_system_partition(info)
    if partitie:
        result["fs_type"] = partitie["fstype"]
        result["opslag_gb"] = to_gb(partitie["total"])

    naam = find_primary_interface(info)
    if naam:
        for a in info["network"]["interfaces"][naam]["addrs"]:
            adres = a["address"].split("%")[0]      # Linux plakt soms "%eth0" achter een IPv6-adres
            if a["family"] == psutil.AF_LINK and result["mac"] is None:
                result["mac"] = adres.upper().replace("-", ":")
            elif a["family"] == socket.AF_INET and result["ipv4"] is None:
                result["ipv4"] = adres
            elif a["family"] == socket.AF_INET6:
                if adres.lower().startswith("fe80"):
                    if result["ipv6_linklocal"] is None:
                        result["ipv6_linklocal"] = adres
                elif result["ipv6"] is None:
                    result["ipv6"] = adres
    return result

def get_filtered_info():
    # Volledige meting: basisscript + uitbreiding + filter
    return filter_system_info(add_system_details(collect_system_info()))

if __name__ == "__main__":
    gefilterd = get_filtered_info()
    for sleutel, waarde in gefilterd.items():
        print(f"{sleutel:15} {waarde}")
