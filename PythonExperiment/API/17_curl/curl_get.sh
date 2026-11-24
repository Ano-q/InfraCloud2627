#!/bin/bash
# curl_get.sh ; eval 17: HTTP GET met curl en het resultaat (statuscode) controleren
# Idee van yroosel/IaCExperiments scripts/curl_bash_variables.sh (statuscode in variabele + if/else),
# maar zonder wachtwoord in het script en tegen een publieke JSON API.
# Werkt in Git Bash (Windows) en op de LABVM.
URL=${1:-https://ipinfo.io/country}

date -Iseconds
echo "GET $URL"
# -s stil, -o body naar bestand, -w enkel de HTTP-statuscode teruggeven
status_code=$(curl -s -o /tmp/curl_body.txt -w "%{http_code}" "$URL")
echo "Body   : $(head -c 300 /tmp/curl_body.txt)"
echo "Status : $status_code"

if [ "$status_code" -eq 200 ]; then
   echo "OK - request succeeded (200)"
else
   echo "NOK - unexpected status code: $status_code"
   exit 1
fi

# extra: zelfde request met headers (-i), zoals in de slides
echo "--- curl -i (headers) ---"
curl -s -i "$URL" | head -8
