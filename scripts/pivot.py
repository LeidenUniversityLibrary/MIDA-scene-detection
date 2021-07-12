import pandas as pd
import sys


stacked_file = sys.argv[1]
stacked_data = pd.read_csv(stacked_file).fillna("")
print(stacked_data.head())

pivoted_data = stacked_data.pivot(index="frame", columns="variable", values="value")
pivoted_data["lavfi_ocr_text"] = pivoted_data["lavfi_ocr_text"].astype("string", copy=False)
pivoted_data["lavfi_ocr_confidence"] = pivoted_data["lavfi_ocr_confidence"].astype("string", copy=False)
print(pivoted_data.dtypes)
pivoted_data2 = pivoted_data[["pkt_pts_time", "lavfi_scd_mafd","lavfi_scd_score","lavfi_ocr_confidence","lavfi_ocr_text"]]
good_rows = pivoted_data2["lavfi_ocr_confidence"].notna()
pivoted_data2["confidences"] = pivoted_data2.loc[good_rows, "lavfi_ocr_confidence"].str.strip().str.split(" ").apply(lambda str_list: [int(x) for x in str_list])
# Create summary statistics for word confidence scores
confidences_stats = pivoted_data2.loc[good_rows, "confidences"].apply(lambda num_list: pd.Series(num_list).describe())
print(pivoted_data2.head())
print(confidences_stats.head())
pivoted_data2["nr_words"] = pivoted_data2.loc[good_rows, "confidences"].apply(len)
pivoted_data2["nr_lines"] = pivoted_data2.loc[good_rows, "lavfi_ocr_text"].str.count(r'\\n')
pivoted_data3 = pivoted_data2.join(confidences_stats)
print(pivoted_data3.loc[good_rows, :].head())
pivoted_file = stacked_file.replace(".csv", "-p.csv")
pivoted_data3.to_csv(pivoted_file)
