import os
import glob
import pandas as pd
os.chdir("../")
os.chdir("FinalDataset/")
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
combined_csv.to_csv("feature_data.csv")