# MIDA scene detection and extraction, and OCR tools

This repository contains scripts for some analysis of Payitaht Abdülhamid.
Data files are stored separately in SURFdrive.

## Installation

Each tool may have different dependencies.
They have been developed for use in a Linux or MacOS environment and are not
guaranteed to work on other platforms.

Most tools rely on Python and [Pandas].
Video analysis (e.g. shot change detection) and frame extraction use [ffmpeg].
OCR requires [ffmpeg] with [Tesseract] support, and [tesseract-lang] to be
installed.
Older scripts use (GNU) [sed] and [GNU awk].

[Pandas]: https://pandas.pydata.org/
[ffmpeg]: https://ffmpeg.org
[Tesseract]: https://github.com/tesseract-ocr/tesseract
[tesseract-lang]: https://github.com/tesseract-ocr/tessdata
[sed]: https://www.gnu.org/software/sed/manual/sed.html
[GNU awk]: https://www.gnu.org/software/gawk/manual/gawk.html

## Usage

This repository has scripts that help you:

- detect scene (i.e. shot) changes
- convert ffmpeg "flat format" output to CSV files
- run OCR on videos with Arabic subtitles
- convert timestamps from hours:minutes:seconds to seconds
- align approximate timestamps to detected scenes
- generate scripts to extract all frames from selected scenes as images

### Detect scene (i.e. shot) changes

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

### Run OCR to extract subtitles from frames

Previous attempts have been documented in the [OCR docs](docs/ocr.md).

The most current commands have been listed in the `ocr-run.sh` script.

[ocr]: https://ffmpeg.org/ffmpeg-filters.html#ocr

### Convert ffmpeg "flat output" to CSV

Use the `flat-to-csv.sh` script:

```sh
./flat-to-csv.sh INPUT_FILE [OUTPUT_FILE]
```

### Convert ffmpeg frames.txt to CSV (deprecated)

This is no longer necessary, since ffmpeg is set to output in its "flat
format".

```sh
awk -f scripts/frames-to-csv.awk episodes/1/data_out/frames.txt > episodes/1/data_manual/scenes.csv
```

### Select rows from CSV (deprecated)

Using [csvkit], I can find the rows that have been marked to contain the
Star of David.
This query works for small files, in which I manually aligned the manual
timestamps with the scene times.

```sh
csvsql --query 'select * from scenes_david where david is not NULL' -v data_manual/scenes_david.csv
```

[csvkit]: https://csvkit.readthedocs.io/en/latest/

### Merge manual marks with scenes (deprecated)

The manual marks indicate rough timestamps at which a Star of David is visible.
I want to link these timestamps to detected scenes so that I can extract frames
from the whole scene, to help provide training data.

```sh
cd episodes/$EPISODE
csvsql --query 'select s.*, m.* from scenes s, david1 m where s.start_ms <= m.ms and s.end_ms >= m.ms' \
    -v data_manual/scenes.csv data_manual/david1.csv > data_manual/merged_marks.csv
```

There is an error in my assumption that I need only the scenes in which the
`123000` millisecond falls. Instead I need all scenes that cover
`[123000,124000)`.

```sh
cd episodes/$EPISODE
csvsql --query 'select s.*, m.s from scenes s, david2 m where (s.start_ms <= m.ms and s.end_ms >= m.ms) or (s.start_ms <= m.ms + 999 and s.end_ms >= m.ms + 999)' \
    -v data_manual/scenes.csv data_manual/david2.csv > data_manual/merged_marks2.csv
```

In ELAN, I checked which of the adjourning scenes actually contain the symbol.
I exported these annotations as TSV with too many columns (and no header, as
ELAN doesn't do headers).
Therefore I need to select the columns I need, in the correct order:

```sh
csvcut -t -H -c 12,4,7 data_manual/2-annotations.tsv > data_manual/adjusted_marks.csv
```

I then add a header to this file and create the script to extract scenes.

### Extract scenes (deprecated old way)

```sh
cd episodes/1/
ffmpeg -report -ss 165927ms -to 167087ms -i data/video.webm -vsync 2 data_out/scene-0066/frame-%03d.jpg
```

Create a script that extracts each scene as in the above command:
(note that you have to set the video file name yourself)

```sh
cd episodes/$EPISODE
awk -f ../../scripts/marks-to-sh.awk video=4QIcBbbPojc.mkv data_manual/merged_marks.csv > extract.sh
```

Check for duplicate commands in `extract.sh`, as sometimes multiple manually
identified timestamps may be in the same scene.
The results would the same regardless, but it's wasted time.

## Getting source material

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
