#!/usr/bin/env bash

# Using linux date
# For mac - brew install coreutils ; echo "alias date=gdate" >> ~/.bash_profile
runtime="24 hours"
endtime=$(date -ud "$runtime" +%s)
echo "Collecting docker stats for ${runtime} or until cancelled..."

# while true
while [[ $(date -u +%s) -le ${endtime} ]]
do docker stats --no-stream --format "table {{.Name}};{{.CPUPerc}};{{.MemPerc}};{{.MemUsage}};{{.NetIO}};{{.BlockIO}};{{.PIDs}}" > dockerstats
tail -n +2 dockerstats | awk -v date=";$(date -u +'%Y-%m-%dT%H:%M:%SZ')" '{print $0, date}' >> data.csv
sleep 1
done

echo "Finished after ${runtime} see data.csv"
rm -rf dockerstats
