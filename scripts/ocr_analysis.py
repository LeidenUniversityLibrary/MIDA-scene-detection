import pandas as pd
import sys


# Read file name from arguments and load
pivoted_file = sys.argv[1]
csv_dtypes = {
    "frame": "int64",
    "pkt_pts_time": "float64",
    "lavfi_scd_mafd": "float64",
    "lavfi_scd_score": "float64",
    "lavfi_ocr_text": "string",
    "lavfi_ocr_confidence": "string"
}
pivoted_data = pd.read_csv(pivoted_file, dtype = csv_dtypes)

# pivoted_data["lavfi_ocr_text"] = pivoted_data["lavfi_ocr_text"].astype("string", copy=False)
# pivoted_data["lavfi_ocr_confidence"] = pivoted_data["lavfi_ocr_confidence"].astype("string", copy=False)
print(pivoted_data.dtypes)
pivoted_data2 = pivoted_data.copy()[["pkt_pts_time", "lavfi_scd_mafd","lavfi_scd_score","lavfi_ocr_confidence","lavfi_ocr_text"]]
good_rows = pivoted_data2["lavfi_ocr_confidence"].notna()
pivoted_data2.loc[:, "confidences"] = pivoted_data2.loc[good_rows, "lavfi_ocr_confidence"].str.strip().str.split(" ").apply(lambda str_list: [int(x) for x in str_list])
# The original unparsed OCR confidences are no longer needed
del pivoted_data2["lavfi_ocr_confidence"]
# Create summary statistics for word confidence scores
confidences_stats = pivoted_data2.loc[good_rows, "confidences"].apply(lambda num_list: pd.Series(num_list).describe())
# Count number of `\n` occurrences as number of recognised lines
pivoted_data2["nr_lines"] = pivoted_data2.loc[good_rows, "lavfi_ocr_text"].str.count(r'\\n')
pivoted_data3 = pivoted_data2.join(confidences_stats)
print(pivoted_data3.loc[good_rows, :].head())
analysed_file = pivoted_file.replace(".csv", "-a.csv")
pivoted_data3.to_csv(analysed_file)
