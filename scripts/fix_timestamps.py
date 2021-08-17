# Convert HH:mm:ss timestamps to ss.0 seconds
import pandas as pd
import sys


# Read file name from arguments and load
timestamps_filename = sys.argv[1]
csv_dtypes = {
    "start": "string",
    "end": "string",
    "count": "string"
}
timestamps_data = pd.read_csv(timestamps_filename, dtype = csv_dtypes)
print(timestamps_data)

def convert_hms_to_seconds(hms: pd.Series) -> pd.Series:
    hms_list = hms.str.replace(":","").str.extract(r"(?P<h>\d\d)?(?P<m>\d\d)(?P<s>\d\d)").astype("Int64")
    return hms_list.s + hms_list.m * 60 + hms_list.h.fillna(0) * 3600

fixed_data = timestamps_data.assign(start_s=convert_hms_to_seconds(timestamps_data.start),
end_s=convert_hms_to_seconds(timestamps_data.end))

print(fixed_data)

out_filename = timestamps_filename.replace(".csv", "-seconds.csv")
if len(sys.argv) > 2:
    out_filename = sys.argv[2]
fixed_data.to_csv(out_filename)
