#!/bin/sh
set -e;

VIDEO=$1
FOLDER=$2
LENGTH=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 ${FOLDER}/${VIDEO})

number_of_frames=$(ffprobe -v error -show_entries stream=nb_frames -select_streams v -of default=noprint_wrappers=1:nokey=1 ${FOLDER}/${VIDEO})
echo "Total number of frames: ${number_of_frames}"
REDFACTOR=10
# It looks like all videos have the same 25 fps framerate, so we don't need to
# use it in calculating the number of seconds we need to extract to each folder
# framerate=$(ffprobe -v error -show_entries stream=r_frame_rate -select_streams v -of default=noprint_wrappers=1:nokey=1 ${FOLDER}/${VIDEO})
folders=$(( (${number_of_frames}/${REDFACTOR}) / 1000))
echo ${folders}
iterations=$((${LENGTH%.*} / 400))
echo $iterations
if [[ ${folders} -ne ${iterations} ]]; then
    echo "Something is wrong in the calculations, exiting"
    exit 1
fi

for START in $(seq 0 $iterations); do
    ST=$((${START} * 400))
    mkdir -p ${FOLDER}/all_frames/${START}
    echo "Starting extraction at $ST seconds"
    ffmpeg -hide_banner -v error -ss ${ST}.0 -t 400.0 -i ${FOLDER}/${VIDEO} -vsync 0 -copyts -lavfi select="not(mod(n\,${REDFACTOR}))" -frame_pts true -qscale:v 1 -qmin 1 -qmax 1 ${FOLDER}/all_frames/${START}/f-%06d.jpg
done
