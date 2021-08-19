# Create a shell script to extract scenes
import pandas as pd
import sys


# Read file name from arguments and load
timestamps_filename = sys.argv[1]
ts_dtypes = {
    "scene": "int64",
    "start": "float64",
    "end": "float64",
    "pentagram_visible": "int64"
}
timestamps_data = pd.read_csv(timestamps_filename, dtype = ts_dtypes, usecols=["scene","pentagram_visible","start","end"])
print(timestamps_data.head(10))
print(timestamps_data.dtypes)
video_file = sys.argv[2]


def print_extract_scene(scene: pd.Series):
    if scene["pentagram_visible"] == 1:
        label = "pentagram"
    else:
        label = "no_pentagram"
    scene_nr = round(scene["scene"])
    result = "mkdir -p frames_by_class/{}/s-{:0<4d}\n".format(label, scene_nr)
    result += "ffmpeg -ss {} -to {} ".format(scene["start"], scene["end"])
    result += "-i data/{} -copyts -frame_pts true frames_by_class/{}/s-{:0<4d}/f-%d.jpg\n".format(video_file, label, scene_nr)
    return result

out_filename = "extract.sh"
if len(sys.argv) > 3:
    out_filename = sys.argv[3]
with open(out_filename, "w") as f:
    for idx, row in timestamps_data.iterrows():
        f.write(print_extract_scene(row))
