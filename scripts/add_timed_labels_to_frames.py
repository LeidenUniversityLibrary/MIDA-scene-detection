"""Add label columns to frames for training a multi-hot model.

Usage::

    $ python add_timed_labels_to_frames.py frames-with-scenes.csv <timed-annotations.csv> <output.csv>

"""
import pandas as pd
import pandasql as ps
import sys


# Read file names from arguments
frames_file = sys.argv[1]
anno_file = sys.argv[2]
output_file = sys.argv[3]

# Load frames data
csv_dtypes = {
    "frame": "int64",
    "scene": "int64",
    "pkt_pts_time": "float64"
}
use_cols = ["frame","pkt_pts_time","scene"]
frames_data = pd.read_csv(frames_file, dtype = csv_dtypes, index_col="frame", usecols=use_cols)
print(frames_data.head())


# Add column for frame filename
def derive_filename(row):
    frame_nr = str(row.name).rjust(6, "0")
    filename = f'{frame_nr[:2]}/{frame_nr[2:4]}/f-{frame_nr}.jpg'
    return filename

frames_data.loc[:, 'filename'] = frames_data.apply(derive_filename, axis=1)

# Load scene data
anno_data = pd.read_csv(anno_file, usecols=lambda x: not x.startswith("Unnamed"))
anno_data.rename({"Begin Time - ss.msec": "anno_start", "End Time - ss.msec": "anno_end"}, axis="columns", inplace=True)
print(anno_data.head())

# Join the scene labels with the original frame list
join_query = '''
select *
from frames_data f 
left join anno_data a
on f.pkt_pts_time >= a.anno_start and f.pkt_pts_time < a.anno_end
'''

frames_with_labels = ps.sqldf(join_query, locals()).set_index("frame")
frames_with_labels.loc[frames_with_labels["pentagram"].notna(), "pentagram_visible"] = 1.0
frames_with_labels.loc[frames_with_labels["star"].notna(), "star_visible"] = 1.0
print(frames_with_labels.head())
frames_with_labels.to_csv(output_file)


