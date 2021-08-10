import pandas as pd
import sys


# Read file name from arguments and load
pivoted_file = sys.argv[1]
csv_dtypes = {
    "frame": "int64",
    "pkt_pts_time": "float64",
    "lavfi_scd_mafd": "float64",
    "lavfi_scd_score": "float64",
    "lavfi_scd_time": "float64",
    "lavfi_blackframe_pblack": "float64"
}
use_cols = ["frame","pkt_pts_time","lavfi_scd_mafd","lavfi_scd_score","lavfi_scd_time","lavfi_blackframe_pblack"]
frames_data = pd.read_csv(pivoted_file, dtype = csv_dtypes, index_col="frame", usecols=use_cols)

# Make sure the first frame starts a scene by setting the `scd_time`
frames_data.loc[0, "lavfi_scd_time"] = 0.0

# Black frames should start new scenes too
frames_data.loc[:, "black_frames"] = frames_data["lavfi_blackframe_pblack"].rolling(2, min_periods=1, center=True).count()
frames_data.loc[frames_data.black_frames == 1.0, "lavfi_scd_time"] = frames_data.pkt_pts_time

# Fill down the scene detection time to allow grouping frames by scene
frames_data["lavfi_scd_time"].fillna(method="pad", inplace=True)

scene_numbers = frames_data.groupby("lavfi_scd_time").ngroup()
print(scene_numbers.head())

# Join the scene indices with the original frame list
frames_with_scenes = frames_data.assign(scene=scene_numbers)
print(frames_with_scenes.head())
enriched_file = pivoted_file.replace(".csv", "-with-scenes.csv")
frames_with_scenes.to_csv(enriched_file)

# Determine length of scenes
frames_by_scene = frames_data.reset_index().groupby("lavfi_scd_time")
scene_sizes = frames_by_scene.size()
print(scene_sizes.head())

frame_duration = frames_data.loc[1, "pkt_pts_time"]

scenes = frames_by_scene.agg(
    last_pts=("pkt_pts_time", "max"),
    duration=("pkt_pts_time", lambda x: round(x.max() - x.min() + frame_duration, 5)),
    first_frame=("frame", "min"),
    last_frame=("frame", "max")
    )\
    .assign(number_of_frames=scene_sizes,
    low_mafd=frames_by_scene["lavfi_scd_mafd"].quantile(0.2).round(5),
    median_mafd=frames_by_scene["lavfi_scd_mafd"].quantile(0.5).round(5),
    high_mafd=frames_by_scene["lavfi_scd_mafd"].quantile(0.8).round(5),
    high95_mafd=frames_by_scene["lavfi_scd_mafd"].quantile(0.95).round(5),
    scd_score=frames_by_scene["lavfi_scd_score"].first())\
    .reset_index()
scenes.index.name = "scene"
print(scenes.head())

# Save the scenes information to a new file based on the input file name
analysed_file = pivoted_file.replace(".csv", "-scenes.csv")
scenes.to_csv(analysed_file)
