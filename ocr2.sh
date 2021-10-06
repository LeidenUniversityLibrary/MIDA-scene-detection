#!/bin/sh

set -e

# Usage: SCRIPT INPUT_VIDEO OUTPUT_DIR LANGUAGE
# The RUN is an identifier to help us keep apart multiple runs of the same script
IN_FILE=$1
OUT_DIR=$2
LANGUAGE=$3
# mkdir -p ${OUT_DIR}

export FFREPORT="file=${OUT_DIR}/ffprobe-report.log"
OUT_FLAT_TXT="${OUT_DIR}/ffprobe-flat.txt"
FFERR="${OUT_DIR}/ffprobe-output.log"

# Run OCR
ffprobe -f lavfi -i movie=${IN_FILE},ocr=language=${LANGUAGE}:whitelist='',scdet=threshold=6.0 \
 -show_entries frame=pkt_pts_time:frame_tags=lavfi.scd.mafd,lavfi.scd.score,lavfi.ocr.text,lavfi.ocr.confidence \
 -print_format flat > ${OUT_FLAT_TXT} 2> ${FFERR}
