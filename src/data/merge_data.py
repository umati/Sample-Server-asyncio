import pandas as pd
import glob
import os

pattern = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datasets", "*.csv")

dframes = [pd.read_csv(csv) for csv in glob.glob(pattern)]
# dframes = []
# for csv in glob.glob(pattern):
#     try:
#         data = pd.read_csv(csv)
#         print("Successful:", csv)
#         print(data)
#     except Exception:
#         data = None
#         print("Error:", csv)
#     if data is not None:
#         dframes.append(data)
all_df = pd.concat(dframes, axis=1)
all_df.to_csv(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.csv")))
print("Created: data.csv")
