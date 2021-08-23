#!/bin/sh

# Usage: SCRIPT INPUT_VIDEO RUN
# The RUN is an identifier to help us keep apart multiple runs of the same script
IN_FILE=$1
OUT_DIR="scene-detection/$2"

OUT_FLAT_TXT="${OUT_DIR}/ffprobe-flat.txt"
FRAMES_WIDE="${OUT_DIR}/frames-wide.csv"
FRAMES_WITH_SCENE="${OUT_DIR}/frames-with-scene.csv"
SCENES_ANALYSED="${OUT_DIR}/scenes-analysed.csv"

# Detect scenes
$(dirname $0)/scdet.sh ${IN_FILE} $2

# Convert flat output to CSV
$(dirname $0)/flat-to-csv.sh ${OUT_FLAT_TXT}

# Mark scenes with frames
python3 $(dirname $0)/scripts/mark_scenes.py ${FRAMES_WIDE} ${FRAMES_WITH_SCENE} ${SCENES_ANALYSED}
