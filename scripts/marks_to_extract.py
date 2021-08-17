# Create a shell script to extract scenes
import pandas as pd
import sys


# Read file name from arguments and load
timestamps_filename = sys.argv[1]
ts_dtypes = {
    "scene": "int64",
    "lavfi_scd_time": "float64",
    "end_time": "float64",
    "count": "string"
}
timestamps_data = pd.read_csv(timestamps_filename, dtype = ts_dtypes, usecols=["scene","count","lavfi_scd_time","end_time"])
print(timestamps_data)

video_file = sys.argv[2]


def print_extract_scene(scene: pd.Series):
    result = "mkdir -p data_out/scene-{}\n".format(scene["scene"])
    result += "ffmpeg -report -ss {} -to {} ".format(scene["lavfi_scd_time"], scene["end_time"])
    result += "-i data/{} -copyts -frame_pts true data_out/scene-{}/frame-%d.jpg\n".format(video_file, scene["scene"])
    return result

with open("extract.sh", "w") as f:
    for idx, row in timestamps_data.iterrows():
        f.write(print_extract_scene(row))
