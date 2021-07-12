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
print(pivoted_data2.head())
pivoted_data2["nr_words"] = pivoted_data2.loc[good_rows, "confidences"].apply(len)
pivoted_data2["nr_lines"] = pivoted_data2.loc[good_rows, "lavfi_ocr_text"].str.count(r'\\n')
print(pivoted_data2.loc[good_rows, :].head())
pivoted_file = stacked_file.replace(".csv", "-p.csv")
pivoted_data2.to_csv(pivoted_file)
