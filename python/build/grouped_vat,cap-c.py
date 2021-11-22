if True:
  import pandas as pd
  import numpy as np
  import re # regex


grouped = pd.read_csv (
  "config/vat/grouped/1.dos2unix/vat-by-capitulo-c.tsv",
  sep = "\t" )
