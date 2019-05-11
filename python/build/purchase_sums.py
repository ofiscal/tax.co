# This program sums purchases within person.
import sys
import python.build.output_io as oio
import python.common.misc as c
import python.common.cl_args as c


purchases = oio.readStage(
  c.subsample, "purchases_2_vat."           + c.strategy_suffix )

# extract the predial tax
purchases["predial"] = (purchases["coicop"] == 12700601) * purchases["value"]

purchases["transactions"] = 1 # useful when summed
purchase_sums = purchases.groupby( ["household", "household-member"]
         ) [ "value"
           , "transactions"
           , "vat paid, max"
           , "vat paid, min"
           , "predial"
         ] . agg("sum")
purchase_sums = purchase_sums.reset_index(
  level = ["household", "household-member"] )

oio.saveStage( c.subsample
             , purchase_sums
             , "purchase_sums." + c.strategy_suffix )
