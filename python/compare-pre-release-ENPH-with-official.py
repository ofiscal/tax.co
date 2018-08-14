import pandas as pd

old_folder = "data/enph-2017/pre-publication/recip-100/"
new_folder = "data/enph-2017/recip-100/"

def old_columns(filename):
  x = pd.read_csv(old_folder + filename + ".csv")
  return x.columns

old = st2_sea_enc_gcfhr_ce_csv
