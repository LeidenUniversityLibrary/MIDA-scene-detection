#!/bin/sh
# Turn ffprobe's flat format into proper CSV

IN_FILE=$1
OUT_CSV=${IN_FILE%.txt}.csv

echo "frame,variable,value" > ${OUT_CSV}
sed -E -f $(dirname $0)/scripts/cleanup.txt ${IN_FILE} >> ${OUT_CSV}

python3 $(dirname $0)/scripts/pivot.py ${OUT_CSV}
