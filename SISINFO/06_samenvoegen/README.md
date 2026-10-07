# 06 - Samenvoegen

`merge_team_csv.py` reads every `sysinfo_*.csv` in `output/team_csv/` and writes them to `output/team_sysinfo.csv`. It reports missing columns. Duplicates are matched by serial number, or by computer name if there is none. To add a team member, put their CSV in `output/team_csv/` and run the script again.
