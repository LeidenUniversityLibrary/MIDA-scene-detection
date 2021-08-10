#!/bin/sh

IN_FILE=$1

OUTPUT_TXT=${IN_FILE%.*}-$(date +"%Y%m%d%H%M%S").txt
SCD_THRESHOLD=4.5

CMD="ffprobe -report"
CMD="${CMD} -f lavfi -i movie=${IN_FILE},scdet=threshold=${SCD_THRESHOLD},blackframe=amount=99:threshold=24,signalstats -show_entries frame=pkt_pts_time,width,height:frame_tags -print_format flat"
echo ${CMD}
echo "Output: ${OUTPUT_TXT}"
${CMD}  > ${OUTPUT_TXT} 2> ${OUTPUT_TXT}-err.log
