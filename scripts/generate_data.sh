#!/usr/bin/env bash

#while true; do docker stats --no-stream > dockerstats; tail -n +2 dockerstats >> data.txt; sleep 5; done
while true
do docker stats --no-stream --format "table {{.Name}};{{.CPUPerc}};{{.MemPerc}};{{.MemUsage}};{{.NetIO}};{{.BlockIO}};{{.PIDs}}" > dockerstats
tail -n +2 dockerstats | awk -v date=";$(date +%T)" '{print $0, date}' >> data.csv
sleep 5
done