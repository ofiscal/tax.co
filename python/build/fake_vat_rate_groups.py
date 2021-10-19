# This writes three files, of two kinds:
# (1) New, fake VAT data, equal to the original but
#     with a new random integer column called "rate group".
#     There are two such files, for COICOP and for Capitulo C.
# (2) A "rate_groups" file, which assigns a VAT rate to each group.

import numpy as np
import pandas as pd
import os


source_folder      = "config/vat/"
destination_folder = os.path.join ( source_folder, "fake_grouped" )
number_of_rate_groups = 3

# PITFALL: IO: Writes a new file.
def add_fake_rate_group_column ( vat_filename : str ) -> pd.DataFrame:
  df = pd.read_csv (
    os.path.join ( source_folder, vat_filename ),
    encoding = "latin1" )
  df["rate group"] = np.random.randint (
    0, number_of_rate_groups, len ( df ) )
  df.to_csv( os.path.join ( "config/vat/fake_grouped", vat_filename ),
             index = False )
  return df

coicop = add_fake_rate_group_column ( "vat_by_coicop.csv" )
capitulo_c = add_fake_rate_group_column ( "vat_by_capitulo_c.csv" )

rate_groups = pd.DataFrame (
  [ [ 0, 0 ],
    [ 1, 0.05 ],
    [ 2, 0.19 ], ],
  columns = ["rate group", "rate" ] )
rate_groups.to_csv (
  os.path.join ( destination_folder, "rate_groups.csv" ),
  index = False )

consumable_groups = pd.DataFrame (
  [ [ "food",          0 ] ,
    [ "medicine",      1 ] ,
    [ "travel",        2 ] ,
    [ "entertainment", 2 ] , ],
  columns = ["consumable group", "rate group" ] )
consumable_groups.to_csv (
  os.path.join ( destination_folder, "consumable_groups.csv" ),
  index = False )
