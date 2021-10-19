# How I created these

import numpy as np
import os
import pandas as pd

table_kinds = [ "coicop", "capitulo_c" ]
tables = {}
for tk in table_kinds:
  tables [ tk ] = pd.read_csv (
    os.path.join (
      "config/vat",
      "vat_by_" + tk + ".csv" ) )
  t = tables [tk]
  t ["group"] = pd.Series (
    np.random.randint( 0, 5, len(t) ) )
  t.to_csv (
    os.path.join (
      "/mnt/tax_co/config/vat/fake_grouped",
      "vat_by_" + tk + ".csv" ) )
