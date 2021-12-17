"""
Add label columns to frames for predicting using a multi-hot model.

Usage::

    $ python add_empty_labels_to_frames.py frames-with-scenes.csv <label1,label2> <output.csv>

"""
import pandas as pd
import sys


# Read file names from arguments
frames_file = sys.argv[1]
labels = sys.argv[2]
output_file = sys.argv[3]

# Load frames data
csv_dtypes = {
    "frame": "int64",
    "scene": "int64",
    "pkt_pts_time": "float64",
    "lavfi_scd_mafd": "float64",
    "lavfi_scd_score": "float64",
    "lavfi_scd_time": "float64",
    "lavfi_blackframe_pblack": "float64"
}
use_cols = ["frame","pkt_pts_time","scene","lavfi_scd_mafd","lavfi_scd_score","lavfi_scd_time"]
frames_data = pd.read_csv(frames_file, dtype = csv_dtypes, index_col="frame", usecols=use_cols)
print(frames_data.head())


# Add column for frame filename
def derive_filename(row):
    frame_nr = str(row.name).rjust(6, "0")
    filename = f'{frame_nr[:2]}/{frame_nr[2:4]}/f-{frame_nr}.jpg'
    return filename

frames_data.loc[:, 'filename'] = frames_data.apply(derive_filename, axis=1)

for l in labels.split(','):
    col_name = l + "_visible"
    frames_data.loc[:, col_name] = pd.NA

print(frames_data.head())
frames_data.to_csv(output_file)
