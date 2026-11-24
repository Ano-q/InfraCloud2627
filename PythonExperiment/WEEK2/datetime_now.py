#datetime_now.py ; week 2 opdracht 4: Python datetime
# Aangepast van yroosel/PythonExperiments mixed/print_date.py (+ DOCU Sep30-2026 "Date & Time")
# Tip uit de les: elk script start met datum en tijd -> zo bewijst de uitvoer wanneer het gedraaid heeft.
import datetime

now = datetime.datetime.now()
print("Current date and time:", now)
print("ISO 8601            :", now.isoformat(timespec="seconds"))
print("Formatted (strftime):", now.strftime("%d/%m/%Y %H:%M:%S"))
print("Day of the week     :", now.strftime("%A"))
exam = datetime.datetime(2026, 11, 25, 9, 0)
print("Time until exam     :", exam - now)          # timedelta = verschil tussen twee datetimes
