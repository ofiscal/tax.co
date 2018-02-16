import pandas as pd

folder = "data/enig-2007/"
data = pd.read_csv(     folder + "recip-1/" + "Ig_ml_hogar.txt", sep='\t', encoding='latin_1')
