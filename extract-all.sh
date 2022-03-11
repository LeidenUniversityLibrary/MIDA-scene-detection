#!/bin/sh
set -e;

VIDEO=$1
FRAMES_CSV=$2
FOLDER=$3
LENGTH=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 ${FOLDER}/${VIDEO})

number_of_frames=$(ffprobe -v error -show_entries stream=nb_frames -select_streams v -of default=noprint_wrappers=1:nokey=1 ${FOLDER}/${VIDEO})
echo "Total number of frames: ${number_of_frames}"
folders=${number_of_frames%[0-9][0-9][0-9][0-9]}
# echo ${folders}
iterations=$((${LENGTH%.*} / 300))
# echo $iterations
# exit 0

for f in $(seq -w 0 $folders); do
    for sf in $(seq -w 0 99); do
        mkdir -p ${FOLDER}/all_frames/${f}/${sf}
    done
done
mkdir -p ${FOLDER}/all_frames/tmp
# exit 0
for START in $(seq 0 $iterations); do
    ST=$((${START} * 300))
    echo "Starting extraction at $ST seconds"
    ffmpeg -hide_banner -loglevel level+quiet -ss ${ST}.0 -t 300.0 -i ${FOLDER}/${VIDEO} -vsync 0 -copyts -lavfi select='not(mod(n\,10))' -frame_pts true -qscale:v 1 -qmin 1 -qmax 1 ${FOLDER}/all_frames/tmp/f-%06d.jpg
    echo "Moving files"
    # Inspired by https://unix.stackexchange.com/a/97782/256251
    for FILE in `ls ${FOLDER}/all_frames/tmp`; do
    # f="$(basename $FILE)"
    f="${FILE%.jpg}"
    numbers="${f#f-}"
    firstfour="${numbers%[0-9][0-9]}"
    firsttwo="${firstfour%[0-9][0-9]}"
    secondtwo="${firstfour#[0-9][0-9]}"

    mv "${FOLDER}/all_frames/tmp/$FILE" "${FOLDER}/all_frames/${firsttwo}/${secondtwo}/"
    done
    # parallel 'mv all_frames/tmp/f-{1}{2}??.jpg all_frames/{1}/{2}/' ::: {00..23} ::: {00..75}
done

# ffmpeg -hide_banner -loglevel level+quiet -ss 300.0 -t 300.0 -i data/Blm3j806lkE.mp4 -copyts -frame_pts true all_frames/tmp/f-%06d.jpg
# ffmpeg -hide_banner -loglevel level+quiet -ss 300.0 -t 300.0 -i data/Blm3j806lkE.mp4 -r 1 -copyts -frame_pts true all_frames/tmp/f-%06d.jpg
# ffmpeg -hide_banner -loglevel level+quiet -ss 300.0 -t 300.0 -i data/Blm3j806lkE.mp4 -copyts -frame_pts true -r 1 all_frames/tmp/f-%06d.jpg
# ffmpeg -hide_banner -loglevel level+quiet -ss 300.0 -t 300.0 -i data/Blm3j806lkE.mp4 -vsync 0 -copyts -frame_pts true -r 1 all_frames/tmp/f-%06d.jpg
# ffmpeg -hide_banner -loglevel level+quiet -ss 300.0 -t 300.0 -i data/Blm3j806lkE.mp4 -vsync 0 -copyts -frame_pts true -framerate 1 all_frames/tmp/f-%06d.jpg
# ffmpeg -hide_banner -loglevel level+quiet -ss 300.0 -t 300.0 -i data/Blm3j806lkE.mp4 -vsync 0 -copyts -lavfi select='not(mod(n\,100))' -frame_pts true all_frames/tmp/f-%06d.jpg
# ffmpeg -hide_banner -loglevel level+quiet -ss 300.0 -t 300.0 -i data/Blm3j806lkE.mp4 -vsync 0 -copyts -lavfi select=key -frame_pts true all_frames/tmp/f-%06d.jpg
# ffmpeg -hide_banner -loglevel level+quiet -ss 300.0 -t 300.0 -i data/Blm3j806lkE.mp4 -vsync 0 -copyts -lavfi select=key -frame_pts true -qscale:v 1 -qmin 1 -qmax 1 all_frames/tmp/f-%06d.jpg



