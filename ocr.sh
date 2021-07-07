#!/bin/sh

# IN_FILE=$1
IN_FILE=data_out/3-binarised-dddddd.mp4

OUTPUT_TXT=${IN_FILE%.*}-$(date +"%Y%m%d%H%M%S").txt

CROP_W=in_w
CROP_H="in_h*0.26"
CROP_X=0
CROP_Y="in_h*0.71"
CROP_FILTER="crop=${CROP_W}:${CROP_H}:${CROP_X}:${CROP_Y}"

SCALE_FILTER="scale=w=iw/2:h=ih/2"

OCR_FILTER="ocr=language=ara:whitelist=''"

CMD="ffprobe -report"
CMD="${CMD} -f lavfi -i movie=${IN_FILE},${CROP_FILTER},${SCALE_FILTER},${OCR_FILTER},scdet=threshold=6.0 -show_entries frame=pkt_pts_time,width,height:frame_tags=lavfi.scd.mafd,lavfi.scd.score,lavfi.ocr.text,lavfi.ocr.confidence -print_format flat"
echo ${CMD}
echo "Output: ${OUTPUT_TXT}"

${CMD}  > ${OUTPUT_TXT}
