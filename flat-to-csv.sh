#!/bin/sh
# Turn ffprobe's flat format into proper CSV

IN_FILE=$1
OUT_CSV=$(dirname $1)/frames-long.csv
PIVOTED_CSV=$(dirname $1)/frames-wide.csv

echo "frame,variable,value" > ${OUT_CSV}
sed -E -f $(dirname $0)/scripts/cleanup.txt ${IN_FILE} >> ${OUT_CSV}

python3 $(dirname $0)/scripts/pivot.py -o ${PIVOTED_CSV} ${OUT_CSV}
