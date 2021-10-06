#!/bin/sh

set -e

# Usage: SCRIPT INPUT_VIDEO RUN LANGUAGE FROM_TOP CROP_HEIGHT
# The RUN is an identifier to help us keep apart multiple runs of the same script
# LANGUAGE: ara, eng
# FROM_TOP: fraction of frame height to use as top of the crop box
# HEIGHT: fraction of frame height to use as height of the crop box
if [ "$#" -ne 7 ]; then
  >&2 echo "Usage: $0 INPUT_VIDEO RUN LANGUAGE FROM_TOP CROP_HEIGHT FRAME_SIZE FRAME_RATE"
  exit 1
fi
IN_FILE=$1
OUT_DIR="ocr/$2"
LANGUAGE=$3
FROM_TOP=$4
CROP_HEIGHT=$5
FRAME_SIZE=$6
FRAME_RATE=$7
mkdir -p ${OUT_DIR}


OUT_VIDEO="${OUT_DIR}/video-${LANGUAGE}.mp4"
OUT_FLAT_TXT="${OUT_DIR}/ffprobe-flat.txt"
FRAMES_WIDE="${OUT_DIR}/frames-wide.csv"
FRAMES_WITH_SCENE="${OUT_DIR}/frames-with-scene.csv"
SCENES_ANALYSED="${OUT_DIR}/scenes-analysed.csv"

# Convert video to cropped inverted video
$(dirname $0)/ocr-preprocess.sh ${IN_FILE} ${OUT_DIR} ${OUT_VIDEO} ${FROM_TOP} ${CROP_HEIGHT} ${FRAME_SIZE} ${FRAME_RATE}

# Run OCR
$(dirname $0)/ocr2.sh ${OUT_VIDEO} ${OUT_DIR} ${LANGUAGE}

# Convert flat output to CSV
$(dirname $0)/flat-to-csv.sh ${OUT_FLAT_TXT}

# Analyse and compact OCR results
# python3 $(dirname $0)/scripts/mark_scenes.py ${FRAMES_WIDE} ${FRAMES_WITH_SCENE} ${SCENES_ANALYSED}
