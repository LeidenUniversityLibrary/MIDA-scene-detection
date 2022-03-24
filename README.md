# MIDA scene detection and extraction, and OCR tools

This repository contains scripts for some analysis of Payitaht Abdülhamid.
Data files are stored separately in SURFdrive.

## Installation

Each script may have different dependencies.
They have been developed for use in a Linux or MacOS environment and are not
guaranteed to work on other platforms.

Most scripts rely on Python, [Pandas] and [Click].
Video analysis (e.g. shot change detection) and frame extraction use [ffmpeg].
OCR requires [ffmpeg] with [Tesseract] support, and [tesseract-lang] to be
installed.
Older scripts use (GNU) [sed] and [GNU awk].

[Pandas]: https://pandas.pydata.org/
[Click]: https://click.palletsprojects.com/
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

Please see the [documentation](docs/index.md) in this repository, or the
[rendered online documentation][online_docs] for usage instructions.

[online_docs]: https://leidenuniversitylibrary.github.io/MIDA-scene-detection/

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

## Authors and license

These scripts have been created by Peter Verhaar and Ben Companjen at
Leiden University Libraries' Centre for Digital Scholarship, in collaboration
with Mustafa Çolak and the Netherlands eScience Center.
Some scripts are heavily based on existing tutorials, for which we do not claim
authorship.

The license is to be determined.
