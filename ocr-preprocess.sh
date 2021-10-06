#!/bin/sh

set -e

# Usage: SCRIPT INPUT_VIDEO OUT_DIR OUT_VIDEO FROM_TOP CROP_HEIGHT
# The RUN is an identifier to help us keep apart multiple runs of the same script
IN_FILE=$1
OUT_DIR=$2
OUT_VIDEO=$3
FROM_TOP=$4
CROP_HEIGHT=$5
FRAME_SIZE=$6
FRAME_RATE=$7

if [ ${FRAME_SIZE} == "1280x720" ]; then
SCALE_FILTER=",scale=w=iw/2:h=ih/2"
else
SCALE_FILTER=""
fi


export FFREPORT="file=${OUT_DIR}/ffmpeg-report.log"
FFERR="${OUT_DIR}/ffprobe-output.log"

# Convert video to cropped inverted video
ffmpeg -i ${IN_FILE} -f lavfi -i "color=#DDDDDD:s=${FRAME_SIZE}" \
 -f lavfi -i color=white:s=${FRAME_SIZE} \
 -f lavfi -i color=black:s=${FRAME_SIZE} \
 -lavfi "threshold,crop=in_w:in_h*${CROP_HEIGHT}:0:in_h*${FROM_TOP}${SCALE_FILTER}" \
 -an -r ${FRAME_RATE} "${OUT_VIDEO}" 2> ${FFERR}

