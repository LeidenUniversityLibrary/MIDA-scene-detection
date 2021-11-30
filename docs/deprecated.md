---
title: Deprecated scripts and commands
---

While we are trying to optimise workflows, we cannot say goodbye to our first
attempts just yet.
Some of them are listed below.

# Convert ffmpeg frames.txt to CSV (deprecated)

This is no longer necessary, since ffmpeg is set to output in its "flat
format".

```sh
awk -f scripts/frames-to-csv.awk episodes/1/data_out/frames.txt > episodes/1/data_manual/scenes.csv
```

# Select rows from CSV (deprecated)

Using [csvkit], I can find the rows that have been marked to contain the
Star of David.
This query works for small files, in which I manually aligned the manual
timestamps with the scene times.

```sh
csvsql --query 'select * from scenes_david where david is not NULL' -v data_manual/scenes_david.csv
```

[csvkit]: https://csvkit.readthedocs.io/en/latest/

# Merge manual marks with scenes (deprecated)

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

# Extract scenes (deprecated old way)

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

