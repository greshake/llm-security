#!/usr/bin/env bash
ENDPOINT="localhost:8007"
INTERVAL="50s"
while true; do
    MESSAGE=$(echo -e "--\n"$(tail /home/velocitatem/.bash_history -n 1 )"\n--\n")
    curl -X POST -H "Content-Type: application/json" -d "$MESSAGE" $ENDPOINT
    sleep $INTERVAL
done
