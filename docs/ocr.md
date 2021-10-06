# Run OCR to extract (Arabic) subtitles from frames

The `ocr.sh` script takes a video file as input that is binarised and has only
black text on a white background.

Run the [ffmpeg OCR filter][ocr] with Arabic as selected language.
By default, ffmpeg only allows ASCII characters to be recognised.
We can override the default by setting `whitelist=''` as an option for the OCR filter.
Do not output the media streams.

```sh
cd episodes/$EPISODE
ffmpeg -report -i data/video.webm -filter_complex "ocr=language=ara:whitelist='',metadata=print:file='data_out/ocr.txt'" -f null out.null
ffmpeg -report -i data/video.webm -filter_complex "crop=in_w:in_h*0.35:0:in_h*0.65,lumakey=0.48:0.39,ocr=language=ara:whitelist='',metadata=print:file='data_out/ocr.txt'" -f null out.null
ffmpeg -report -i data/episode3-ar-subs.mp4 -filter_complex "crop=in_w:in_h*0.35:0:in_h*0.65,lumakey=0.48:0.39,ocr=language=ara:whitelist='',metadata=print:file='data_out/ocr.txt'" -f null out.null
```

## Find a good crop with ffplay

```sh
ffplay -ss 300000ms -t 10000ms -vf "edgedetect=mode=colorize,ocr=language=ara:whitelist='',metadata=print:file='data_out/ocr.txt'" -i data/episode3-ar-subs.mp4

ffplay -ss 300000ms -vf "colorhold=color=white:similarity=0.01,edgedetect=mode=colormix,ocr=language=ara:whitelist='',metadata=print:file='data_out/ocr.txt'" -i data/episode3-ar-subs.mp4
ffplay -ss 300000ms -vf "colorhold=color=white:similarity=0.01" -i data/episode3-ar-subs.mp4
ffplay -ss 300000ms -vf "crop=in_w:in_h*0.35:0:in_h*0.65,colorhold=color=white:similarity=0.01" -i data/episode3-ar-subs.mp4
ffplay -ss 300000ms -vf "crop=in_w:in_h*0.35:0:in_h*0.65,limiter=min=60000,colorhold=color=white:similarity=0.01" -i data/episode3-ar-subs.mp4
ffplay -ss 300000ms -vf "crop=in_w:in_h*0.35:0:in_h*0.65,lumakey=0.5:0.4" -i data/episode3-ar-subs.mp4
ffplay -ss 300000ms -vf "crop=in_w:in_h*0.35:0:in_h*0.65,lumakey=0.48:0.39,ocr=language=ara:whitelist='',metadata=print:file='data_out/ocr.txt'" -i data/episode3-ar-subs.mp4
ffplay -report -ss 300000ms -vf "bbox=min_val=100,ocr=language=ara:whitelist='',metadata=print:file='data_out/ocr.txt'" -i data/episode3-ar-subs.mp4
ffplay -report -ss 300000ms -vf "lutyuv=u=128:v=128,ocr=language=ara:whitelist='',metadata=print:file='data_out/ocr.txt'" -i data/episode3-ar-subs.mp4
```

## Find parameters for creating black text on white background

```sh
ffmpeg -report -f lavfi -i testsrc=s=1280x720 -f lavfi -i color=gray:s=1280x720 -f lavfi -i color=white:s=1280x720 -f lavfi -i color=black:s=1280x720 -lavfi threshold output.avi
ffmpeg -report -ss 300000ms -i data/episode3-ar-subs.mp4 -f lavfi -i color=gray:s=1280x720 -f lavfi -i color=white:s=1280x720 -f lavfi -i color=black:s=1280x720 -lavfi threshold data_out/3-binarised.mp4
ffmpeg -report -ss 300000ms -i data/episode3-ar-subs.mp4 -f lavfi -i "color=#EEEEEE:s=1280x720" -f lavfi -i color=white:s=1280x720 -f lavfi -i color=black:s=1280x720 -lavfi threshold data_out/3-binarised-eeeeee.mp4
ffmpeg -report -ss 300000ms -t 10000ms -i data/episode3-ar-subs.mp4 -f lavfi -i "color=#DDDDDD:s=1280x720" -f lavfi -i color=white:s=1280x720 -f lavfi -i color=black:s=1280x720 -lavfi threshold -an data_out/3-binarised-dddddd.mp4
ffmpeg -report -i data/episode3-ar-subs.mp4 -f lavfi -i "color=#DDDDDD:s=1280x720" -f lavfi -i color=white:s=1280x720 -f lavfi -i color=black:s=1280x720 -lavfi threshold -an -r 25 data_out/3-binarised-dddddd.mp4
```

## Adjust cropping even more

```sh
ffplay -vf "crop=in_w:in_h*0.35:0:in_h*0.65,ocr=language=ara:whitelist='',metadata=print:file='data_out/ocr.txt'" -i data_out/3-binarised-dddddd.mp4
ffplay -ss 300000ms -vf "crop=in_w:in_h*0.35:0:in_h*0.65" -i data_out/3-binarised-dddddd.mp4
# More optimal settings: 26% height starting 71% from the top of the frame
ffplay -ss 300000ms -vf "crop=in_w:in_h*0.26:0:in_h*0.71" -i data_out/3-binarised-dddddd.mp4
# Scale the cropped image
ffplay -ss 350000ms -vf "crop=in_w:in_h*0.26:0:in_h*0.71,scale=w=iw/2:h=ih/2" -i data_out/3-binarised-dddddd.mp4
```

## Output OCR results directly with ffprobe

```sh
ffprobe -report -f lavfi -i movie=data_out/3-binarised-dddddd.mp4,crop=in_w:in_h*0.35:0:in_h*0.65,signalstats,ocr=language=ara:whitelist='',metadata=print:file='data_out/ocr-cropped.txt' -show_entries frame=pkt_pts_time:frame_tags=lavfi.signalstats.YMIN,lavfi.signalstats.YLOW,lavfi.signalstats.YAVG,lavfi.signalstats.YHIGH,lavfi.signalstats.YMAX,lavfi.ocr.text,lavfi.ocr.confidence -print_format csv > data_out/3-dddddd-probe-ocr.csv
ffprobe -report -f lavfi -i movie=data_out/3-binarised-dddddd.mp4,crop=in_w:in_h*0.35:0:in_h*0.65,scale=w=iw/2:h=ih/2,ocr=language=ara:whitelist='',scdet=threshold=6.0 -show_entries frame=pkt_pts_time:frame_tags=lavfi.scd.mafd,lavfi.scd.score,lavfi.ocr.text,lavfi.ocr.confidence -print_format csv > data_out/3-dddddd-probe-scaled-ocr.csv
ffprobe -report -f lavfi -i movie=data_out/3-binarised-dddddd.mp4,crop=in_w:in_h*0.35:0:in_h*0.65,scale=w=iw/2:h=ih/2,ocr=language=ara:whitelist='',scdet=threshold=6.0 -show_entries frame=pkt_pts_time:frame_tags=lavfi.scd.mafd,lavfi.scd.score,lavfi.ocr.text,lavfi.ocr.confidence -print_format csv > data_out/3-dddddd-probe-scaled-ocr.csv
```

[ocr]: https://ffmpeg.org/ffmpeg-filters.html#ocr
