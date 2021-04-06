import pandas as pd
import glob
import os

pattern = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datasets", "*.csv")

dframes = [pd.read_csv(csv, encoding="utf-16") for csv in glob.glob(pattern)]
all_df = pd.concat(dframes, axis=1)
all_df.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.csv"), index=False)
print("Created: data.csv")