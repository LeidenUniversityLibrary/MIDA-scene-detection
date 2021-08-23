#!/bin/sh

IN_FILE=$1
OUT_DIR="scene-detection/$2"
mkdir -p "${OUT_DIR}"

OUTPUT_TXT="${OUT_DIR}/ffprobe-flat.txt"
SCD_THRESHOLD=4.5

export FFREPORT="file=${OUT_DIR}/ffprobe-report.log"
CMD="ffprobe"
CMD="${CMD} -f lavfi -i movie=${IN_FILE},scdet=threshold=${SCD_THRESHOLD},blackframe=amount=99:threshold=24,signalstats -show_entries frame=pkt_pts_time,width,height:frame_tags -print_format flat"
echo ${CMD}
echo "Output: ${OUTPUT_TXT}"
${CMD}  > ${OUTPUT_TXT} 2> ${OUT_DIR}/ffprobe-output.log
