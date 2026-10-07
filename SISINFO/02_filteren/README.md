# 02 - Filteren

| Script | Purpose |
|---|---|
| `system_details.py` | Adds computer model, readable CPU name and serial number (via PowerShell, `/sys` or `sysctl`, depending on the OS). |
| `primary_interface.py` | Finds the interface used for internet traffic. Fallback: the active interface with a usable IPv4 address and the most received traffic. |
| `filter_sysinfo.py` | Reduces everything to one flat row of 13 columns (`KOLOMMEN`). Uses the system partition, sizes in GB, and MAC addresses in uppercase with colons. |
