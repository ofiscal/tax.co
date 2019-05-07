import sys
import python.build.output_io as oio
import python.common.misc as c
import python.common.cl_args as c


if c.vat_strategy == c.del_rosario:
  purchases = oio.readStage(
    c.subsample, "purchases_2_1_del_rosario." + c.vat_strategy_suffix )
else:
  purchases = oio.readStage(
    c.subsample, "purchases_2_vat."           + c.vat_strategy_suffix )

if True: # extract the predial tax
  purchases["predial"] = (purchases["coicop"] == 12700601) * purchases["value"]

if True: # sum purchases within person
  purchases["transactions"] = 1 # useful when summed
  purchase_sums = purchases.groupby( ["household", "household-member"]
           ) [ "value"
             , "transactions"
             , "vat paid, max"
             , "vat paid, min"
             , "predial"
           ] . agg("sum")
  purchase_sums = purchase_sums.reset_index( level = ["household", "household-member"] )

  oio.saveStage( c.subsample, purchase_sums, "purchase_sums." + c.vat_strategy_suffix )
