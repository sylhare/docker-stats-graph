#!/usr/bin/env bash

# Using linux date
# For mac - brew install coreutils ; echo "alias date=gdate" >> ~/.bash_profile
runtime="30 minutes"
endtime=$(date -ud "$runtime" +%s)

# while true
while [[ $(date -u +%s) -le ${endtime} ]]
do docker stats --no-stream --format "table {{.Name}};{{.CPUPerc}};{{.MemPerc}};{{.MemUsage}};{{.NetIO}};{{.BlockIO}};{{.PIDs}}" > dockerstats
tail -n +2 dockerstats | awk -v date=";$(date +%T)" '{print $0, date}' >> data.csv
sleep 5
done

cat data.csv
rm -rf dockerstats