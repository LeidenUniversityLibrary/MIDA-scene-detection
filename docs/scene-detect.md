---
title: Scene detection
---

# Detect scene (i.e. shot) changes

Use the [scdet] filter from ffmpeg.

The `scdet.sh` script wraps the command below and outputs data in the flat
format that can be converted to CSV with `flat-to-csv.sh`.

```sh
cd episodes/$EPISODE
${THIS_REPO}/scdet.sh data/video.ext
# The command and output file name are printed
${THIS_REPO}/flat-to-csv.sh ${OUTPUT_FILE_NAME}
```

Note: Some shots fade-cross instead of using hard cuts.
How should those be handled?

```sh
cd episodes/$EPISODE
# Extract the first frame of each new scene
ffmpeg -report -i data/video.webm -filter_complex "blackframe=amount=99:threshold=24,scdet=threshold=6.0,metadata=select:key=lavfi.scd.time,metadata=print:file='data_out/frames.txt'" -vsync 2 "data_out/scene-%03d.jpg"
# Analyse each frame and determine its blackness and the score for scene change
# Print timestamp, height and width information about the frames and all filter-added tags
ffprobe -report -f lavfi -i "movie=data/kf5USsE6Xq8.webm,blackframe=amount=99:threshold=24,scdet=threshold=5.0" -show_entries "frame=pkt_pts_time,height,width:frame_tags" -print_format flat > data_out/scene-changes.txt
```

[scdet]: https://ffmpeg.org/ffmpeg-filters.html#scdet-1

# Scene detection on ALICE

The [MIDA video analysis] repository contains a SLURM job to run scene
detection on all episodes and save the results to SURFdrive.
These raw results are saved in zip files.

[MIDA video analysis]: https://github.com/LeidenUniversityLibrary/MIDA-video-analysis

To process these raw results into a table of scenes and a table of frames with
scene numbers, change into the directory with the zip files and run:

```sh
for E in {2..54}; do
F=$(ls ep${E}_*.zip)
mkdir -p ${E}
unzip ${F} "ep${E}_ffprobe-flat.txt" -d ${E}
python ~/git/MIDA-scene-detection/scripts/pivot.py -m -o ${E}/frames.csv ${E}/*_ffprobe-flat.txt
python ~/git/MIDA-scene-detection/scripts/mark_scenes.py --output-frames ${E}/frames-with-scenes.csv --output-scenes ${E}/scenes.csv ${E}/frames.csv
rm ${E}/*.txt ${E}/frames.csv
done
```
