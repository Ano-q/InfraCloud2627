#device_info.py ; experiment 3: toestelinformatie verzamelen met Netmiko
import re
import sys
from pathlib import Path

from netmiko import ConnectHandler

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from device import DEVICE


def find(pattern, text, default="Unknown"):
    match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
    return match.group(1).strip() if match else default


def parse_version(output):
    return {
        "hostname": find(r"^(\S+) uptime is", output),
        "uptime": find(r"^\S+ uptime is (.+)$", output),
        "model": find(r"^cisco (\S+) .*processor", output),
        "serial": find(r"Processor board ID (\S+)", output),
        "version": find(r"Cisco IOS XE Software, Version (\S+)", output,
                        find(r"Version ([^,\s]+)", output)),
    }


def parse_interfaces(output):
    # "administratively down" bestaat uit twee woorden, daarom een regex i.p.v. split()
    pattern = r"^(\S+)\s+\S+\s+\S+\s+\S+\s+(administratively down|up|down)\s+(\S+)\s*$"
    return [(m.group(1), m.group(2)) for m in re.finditer(pattern, output, re.MULTILINE)]


def parse_cdp(output):
    # "show cdp neighbors detail" is eenvoudiger te parsen dan de tabelversie
    devices = re.findall(r"Device ID: ?(\S+)", output)
    interfaces = re.findall(r"Interface: (\S+?),", output)
    return list(zip(devices, interfaces))


def parse_routes(output):
    routes = []
    pattern = r"^[A-Z][A-Za-z0-9* ]{0,6}?\s+(\d+\.\d+\.\d+\.\d+/\d+)\s+(.*)$"
    for m in re.finditer(pattern, output, re.MULTILINE):
        prefix, rest = m.groups()
        if "directly connected" in rest:
            next_hop = rest.split(",")[-1].strip()
        else:
            next_hop = find(r"via (\S+?),?$", rest.split(",")[0], rest)
        routes.append((prefix, next_hop))
    return routes


def main():
    connection = ConnectHandler(**DEVICE)
    connection.enable()
    version = parse_version(connection.send_command("show version"))
    interfaces = parse_interfaces(connection.send_command("show ip interface brief"))
    cdp_output = connection.send_command("show cdp neighbors detail")
    routes = parse_routes(connection.send_command("show ip route"))
    connection.disconnect()

    print("Device Information")
    print("------------------")
    print(f"Hostname: {version['hostname']}")
    print(f"Model: Cisco {version['model']}")
    print(f"Serial Number: {version['serial']}")
    print()
    print("Software Information")
    print("--------------------")
    print(f"IOS Version: {version['version']}")
    print(f"System Uptime: {version['uptime']}")
    print()
    print("Interfaces")
    print("----------")
    print(f"Total Interfaces: {len(interfaces)}")
    for name, status in interfaces:
        print(f"{name:<24}{status}")
    print()
    print("Connected Devices (CDP Neighbors)")
    print("-------------")
    if "CDP is not enabled" in cdp_output:
        print("CDP is not enabled")
    for device_id, interface in parse_cdp(cdp_output):
        print(f"{device_id} via {interface}")
    print()
    print("Routing Table")
    print("-------------")
    for prefix, next_hop in routes:
        print(f"{prefix} via {next_hop}")


if __name__ == "__main__":
    main()
