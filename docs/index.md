This repository has scripts that help you:

- detect scene (i.e. shot) changes
- convert ffmpeg "flat format" output to CSV files
- run OCR on videos with Arabic subtitles
- convert timestamps from hours:minutes:seconds to seconds
- align approximate timestamps to detected scenes
- generate scripts to extract all frames from selected scenes as images

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

# Run OCR to extract subtitles from frames

Previous attempts have been documented in the [OCR docs](ocr.md).

The most current commands have been listed in the `ocr-run.sh` script.

[ocr]: https://ffmpeg.org/ffmpeg-filters.html#ocr

# Convert ffmpeg "flat output" to CSV

Use the `flat-to-csv.sh` script:

```sh
./flat-to-csv.sh INPUT_FILE [OUTPUT_FILE]
```

# Getting source material

These tools work on downloaded video files.
This should be allowed for research at academic institutions by European
copyright directive; in the Netherlands this is allowed under Auteurswet
article 15n.

On the command line, we can use [youtube-dl] to download specific videos or
(parts of) playlists.
Youtube-dl is available via Homebrew: `brew install youtube-dl`

[youtube-dl]: https://youtube-dl.org/

```sh
# Download videos in a YouTube playlist
youtube-dl --all-subs -o '%(playlist)s/%(title)s/data/%(id)s.%(ext)s' --playlist-reverse --playlist-start 132 --playlist-end 133 --write-description --write-info-json --write-annotations -w 'https://www.youtube.com/playlist?list=PLge_kMuGwvL8pfyOpLP0hXprI7yQ0L2q-'
# Download a specific video
youtube-dl --all-subs --write-description --write-info-json --write-annotations -w 'https://www.youtube.com/watch?v=ZK9sYnqO2TI'
```
