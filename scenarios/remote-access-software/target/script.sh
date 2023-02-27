#!/usr/bin/env bash
ENDPOINT="localhost:8007"
INTERVAL="5s"
while true; do
    # get the last line of the history commmand and store as a MESSAGE
    MESSAGE=$(cat /home/velocitatem/.bash_history  | tail -n 1)
    curl -X POST -H "Content-Type: application/json" -d "$MESSAGE" $ENDPOINT
    sleep $INTERVAL
done
