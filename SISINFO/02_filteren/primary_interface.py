import os
import sys

# Map SISINFO; de andere taakmappen worden toegevoegd zodat hun scripts importeerbaar zijn
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for map_naam in ['01_basisscript']:
    sys.path.insert(0, os.path.join(ROOT, map_naam))

import socket

def get_default_route_ipv4():
    # Geeft het eigen IPv4-adres waarmee deze computer het internet op gaat (of None).
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))    # bij dit type verbinding (UDP) wordt er niets verstuurd
        return s.getsockname()[0]
    except OSError:
        return None
    finally:
        s.close()

def is_usable_ipv4(address):
    return not (address.startswith("127.") or address.startswith("169.254."))

def find_primary_interface(info):
    interfaces = info["network"]["interfaces"]

    # Criterium 1: de interface met het adres waarlangs het internetverkeer loopt
    route_ip = get_default_route_ipv4()
    if route_ip:
        for name, iface in interfaces.items():
            for a in iface["addrs"]:
                if a["family"] == socket.AF_INET and a["address"] == route_ip:
                    return name

    # Criterium 2: aan + bruikbaar IPv4-adres + meeste ontvangen verkeer
    best_name, best_traffic = None, -1
    for name, iface in interfaces.items():
        if not (iface["stats"] or {}).get("isup"):
            continue
        has_ipv4 = any(a["family"] == socket.AF_INET and is_usable_ipv4(a["address"])
                       for a in iface["addrs"])
        if not has_ipv4:
            continue
        traffic = (iface["io"] or {}).get("bytes_recv", 0)
        if traffic > best_traffic:
            best_name, best_traffic = name, traffic
    return best_name

if __name__ == "__main__":
    from collect_sysinfo import collect_system_info
    print("Primaire interface:", find_primary_interface(collect_system_info()))
