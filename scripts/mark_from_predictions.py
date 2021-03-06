"""
Create timespan annotations from predictions for use in ELAN.

Usage::

    $ python mark_from_predictions.py frame-predictions.csv prediction-elan.csv

"""
import pandas as pd
import sys

COLUMN_SUFFIX = "_pred"

# Read file name from arguments and load
predictions_file = sys.argv[1]
csv_dtypes = {
    "frame": "int64",
    "pkt_pts_time": "float64",
    "lavfi_scd_mafd": "float64",
    "lavfi_scd_score": "float64",
    "lavfi_scd_time": "float64"
}
# use_cols = ["frame","pkt_pts_time","lavfi_scd_mafd","lavfi_scd_score","lavfi_scd_time","lavfi_blackframe_pblack"]
frames_data = pd.read_csv(predictions_file, dtype = csv_dtypes)
# frames_data = pd.read_csv(predictions_file, dtype = csv_dtypes, index_col="frame")

frame_duration = frames_data.loc[1, "pkt_pts_time"]

label_columns = [col_name for col_name in frames_data.columns if col_name.endswith(COLUMN_SUFFIX)]
print(f'Found {label_columns} as columns with predictions.')
print(frames_data.head())

enriched_file = sys.argv[2]
all_anno_frames = []

for label in label_columns:
    col_rounded = label + "_round"
    stem = label[:-len(COLUMN_SUFFIX)]
    anno_bound = stem + "_start"
    change = stem + "_change"

    # Make sure the first frame starts an annotation by setting the `anno_bound`
    frames_data.loc[0, anno_bound] = 0.0

    # Start annotation when predicted probability changes from < 0.5 to > 0.5
    # We use the rounded probability for this
    frames_data.loc[:, change] = frames_data[col_rounded].rolling(2, min_periods=2, center=False).sum()
    frames_data.loc[frames_data[change] == 1.0, anno_bound] = frames_data.pkt_pts_time

    # Fill down the annotation boundary time to allow grouping frames by annotation
    frames_data[anno_bound].fillna(method="pad", inplace=True)

    anno_groups = frames_data.groupby(anno_bound)
    anno_numbers = anno_groups.ngroup()
    positive_annos = anno_groups[change].sum()
    print(anno_numbers.head())
    print(positive_annos.head())

    # Join the annotation indices with the original frame list
    frames_data = frames_data.assign(**{stem+"_anno": anno_numbers})
    print(frames_data.head())

    # Determine length of annotations
    anno_sizes = anno_groups.size()
    print(anno_sizes.head())

    annos = anno_groups.agg(
        last_pts=("pkt_pts_time", "max"),
        duration=("pkt_pts_time", lambda x: round(x.max() - x.min() + frame_duration, 5)),
        first_frame=("frame", "min"),
        last_frame=("frame", "max")
        )\
        .assign(number_of_frames=anno_sizes, change_sum=positive_annos, symbol=stem)\
        .reset_index()
    annos.index.name = "anno"
    annos.rename({anno_bound: "anno_start"}, axis="columns", inplace=True)
    print(annos.head())

    all_anno_frames.append(annos)

# Save the annotations information to a new file based on the input file name
analysed_file = enriched_file.replace(".csv", "-annos.csv")
if len(sys.argv) > 3:
    analysed_file = sys.argv[3]

all_annos = pd.concat(all_anno_frames, ignore_index=True)
all_annos.index.name = "anno_id"
all_annos.query("change_sum > 1.0 & number_of_frames > 25").to_csv(analysed_file)

frames_data.to_csv(enriched_file)
