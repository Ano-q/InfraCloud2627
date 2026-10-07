# SISINFO - System Information Scripting

Collects hardware and network info from a computer, exports it to JSON, CSV and XLSX,
merges the files of the whole team and validates the result.

- Requires: `pip install psutil openpyxl`
- Run the tasks in order (01 to 07). Scripts can be started from any directory.
- All generated files go to `output/` (ignored by Git: it contains serial numbers and MAC addresses).
