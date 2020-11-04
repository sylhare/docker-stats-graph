#!/usr/bin/env bash

while true; do docker stats --no-stream >> data.txt; done