import os
import sys

# Map SISINFO; de andere taakmappen worden toegevoegd zodat hun scripts importeerbaar zijn
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for map_naam in ['01_basisscript']:
    sys.path.insert(0, os.path.join(ROOT, map_naam))

import platform
import subprocess

def run_command(command):
    # Voert een commando uit en geeft de eerste regel van de uitvoer terug (of None als het mislukt).
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=20)
        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        return lines[0] if lines else None
    except Exception:
        return None

def read_file(path):
    # Leest een tekstbestand en geeft de inhoud terug (of None als het niet bestaat).
    try:
        with open(path) as f:
            return f.read().strip() or None
    except Exception:
        return None

def get_computer_model():
    system = platform.system()
    if system == "Windows":
        return run_command(["powershell", "-NoProfile", "-Command",
                            "$c = Get-CimInstance Win32_ComputerSystem; $c.Manufacturer + ' ' + $c.Model"])
    if system == "Linux":
        vendor = read_file("/sys/class/dmi/id/sys_vendor")
        product = read_file("/sys/class/dmi/id/product_name")
        parts = [p for p in (vendor, product) if p]
        return " ".join(parts) if parts else None
    if system == "Darwin":   # Darwin = macOS
        return run_command(["sysctl", "-n", "hw.model"])
    return None

def get_cpu_name(fallback=None):
    system = platform.system()
    name = None
    if system == "Windows":
        name = run_command(["powershell", "-NoProfile", "-Command",
                            "(Get-CimInstance Win32_Processor).Name"])
    elif system == "Linux":
        for line in (read_file("/proc/cpuinfo") or "").splitlines():
            if line.startswith("model name"):
                name = line.split(":", 1)[1].strip()
                break
    elif system == "Darwin":
        name = run_command(["sysctl", "-n", "machdep.cpu.brand_string"])
    # Lukt het niet, dan vallen we terug op wat het basisscript al had.
    return name or fallback or None

ONGELDIGE_SERIENUMMERS = {"", "0", "none", "default string", "to be filled by o.e.m.",
                          "system serial number", "not specified", "not applicable"}

def get_serial_number():
    # Serienummer uit de firmware (SMBIOS); None als het niet lukt of een opvulwaarde is.
    system = platform.system()
    serial = None
    if system == "Windows":
        serial = run_command(["powershell", "-NoProfile", "-Command",
                              "(Get-CimInstance Win32_BIOS).SerialNumber"])
    elif system == "Linux":
        serial = read_file("/sys/class/dmi/id/product_serial")   # enkel leesbaar als root
    elif system == "Darwin":
        try:
            out = subprocess.run(["ioreg", "-c", "IOPlatformExpertDevice", "-d", "2"],
                                 capture_output=True, text=True, timeout=20).stdout
            for line in out.splitlines():
                if "IOPlatformSerialNumber" in line:
                    serial = line.split("=", 1)[1].strip().strip('"')
                    break
        except Exception:
            serial = None
    if serial is None or serial.strip().lower() in ONGELDIGE_SERIENUMMERS:
        return None
    return serial.strip()

def add_system_details(info):
    # De uitbreiding toevoegen aan de dict van het basisscript
    info["system"] = {
        "model": get_computer_model(),
        "cpu_name": get_cpu_name(fallback=info["cpu"]["processor"]),
        "serial": get_serial_number(),
    }
    return info

if __name__ == "__main__":
    from collect_sysinfo import collect_system_info
    info = add_system_details(collect_system_info())
    print(info["system"])
