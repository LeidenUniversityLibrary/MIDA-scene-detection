import pandas as pd
import sys


# Read file name from arguments and load
pivoted_file = sys.argv[1]
csv_dtypes = {
    "frame": "int64",
    "pkt_pts_time": "float64",
    "lavfi_scd_mafd": "float64",
    "lavfi_scd_score": "float64",
    "lavfi_scd_time": "float64"
}
use_cols = ["frame","pkt_pts_time","lavfi_scd_mafd","lavfi_scd_score","lavfi_scd_time"]
pivoted_data = pd.read_csv(pivoted_file, dtype = csv_dtypes, index_col="frame", usecols=use_cols)

# print(pivoted_data.dtypes)

# Make sure the first frame starts a scene by setting the `scd_time`
pivoted_data.loc[0, "lavfi_scd_time"] = 0.0
scene_starts = pivoted_data["lavfi_scd_time"].notna()

# print(pivoted_data.loc[scene_starts, :].reset_index().head())

# Copy rows that start new scenes and number them by resetting the index
scenes = pivoted_data.copy().loc[scene_starts, :].reset_index()
scenes.index.name = "scene"
# Delete the `scd_time` column as its values are the same as `pkt_pts_time`
del scenes["lavfi_scd_time"]
# Save the scenes information to a new file based on the input file name
analysed_file = pivoted_file.replace(".csv", "-scenes.csv")
scenes.to_csv(analysed_file)
