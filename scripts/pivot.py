import pandas as pd
import sys


stacked_file = sys.argv[1]
stacked_data = pd.read_csv(stacked_file).fillna("")
print(stacked_data.head())

pivoted_data = stacked_data.pivot(index="frame", columns="variable", values="value")

pivoted_file = stacked_file.replace(".csv", "-p.csv")
pivoted_data.to_csv(pivoted_file)
