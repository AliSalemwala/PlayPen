#! /bin/bash

readpe --format html $1 | tr -d '\n' | tr '"' "'" > peinfo.txt 
