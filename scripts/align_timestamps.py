# Align manual timestamps with detected scenes
import pandas as pd
import sys


# Read file name from arguments and load
timestamps_filename = sys.argv[1]
ts_dtypes = {
    "start_s": "float64",
    "end_s": "float64",
    "count": "string"
}
timestamps_data = pd.read_csv(timestamps_filename, dtype = ts_dtypes, usecols=["count","start_s","end_s"])
print(timestamps_data)

scenes_filename = sys.argv[2]
sc_dtypes = {
    "scene": "int64",
    "lavfi_scd_score": "float64",
    "duration": "float64"
}
sc_cols = ["scene","lavfi_scd_time","duration"]
scenes_data = pd.read_csv(scenes_filename, dtype=sc_dtypes, usecols=sc_cols)
scenes_data.loc[:, "end_time"] = (scenes_data.lavfi_scd_time + scenes_data.duration)
print(scenes_data.head())


def find_closest_timestamp(target: pd.Series) -> pd.Series:
    """
    Determine which scene has the closest start and end timestamps to the
    target timestamps.
    """
    return scenes_data.assign(start_diff= (scenes_data.lavfi_scd_time - target.start_s).abs(),
                         end_diff= (scenes_data.end_time - target.end_s).abs())\
             .assign(total_diff= lambda x: x.start_diff + x.end_diff)\
             .nsmallest(1, ["total_diff"])\
             .iloc[0]
                        

aligned_timestamps = timestamps_data.join(timestamps_data.apply(find_closest_timestamp, axis=1))
print(aligned_timestamps)

aligned_filename = timestamps_filename.replace(".csv", "-aligned.csv")
aligned_timestamps.round(3).to_csv(aligned_filename, index=False)
