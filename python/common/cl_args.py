import pandas as pd
import sys


vat_strategy_names = [
    "const"
  , "detail"
  , "detail_224"
  , "approx"
  , "finance_ministry"
  , "prop_2018_10_31"
  , "prop_2018_11_29"
  , "del_rosario"
]

[const,detail,detail_224,approx,finance_ministry,prop_2018_10_31,prop_2018_11_29,del_rosario] = \
  vat_strategy_names

subsample = int( sys.argv[1] )

if not subsample in [1,10,100,1000]:
  raise ValueError( "invalid subsample reciprocal: " + str(subsample) )

vat_strategy = sys.argv[2]

if not vat_strategy in vat_strategy_names:
  raise ValueError( "invalid vat_strategy: " + vat_strategy )

if vat_strategy in [const, approx, prop_2018_10_31]:
  vat_flat_rate = float(sys.argv[3])  # float: 0.19, 0.107, etc.
else:
  vat_flat_rate = ""

vat_strategy_suffix = vat_strategy + "_" + str(vat_flat_rate)

# PITFALL: In purchases_2_1_del_rosario, there are 4 command line arguments rather than 3,
# and the third is not `vat_flat_rate`.
if vat_strategy == del_rosario:
  del_rosario_exemption_source = sys.argv[3]
  del_rosario_exemption_count = int( sys.argv[4] )


# Wart: This function is duplicated in cl_fake.py
def collect_files( file_structs, subsample=subsample ):
  acc = pd.DataFrame()
  for f in file_structs:
    shuttle = (
      pd.read_csv(
        "data/enph-2017/recip-" + str(subsample) + "/" + f.filename
        , usecols = list( f.col_dict.keys() )
      ) . rename( columns = f.col_dict      )
    )
    shuttle["file-origin"] = f.name
    for c in f.corrections:
      shuttle = c.correct( shuttle )
    acc = acc.append(shuttle)
  return acc
