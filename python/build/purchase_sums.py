import sys
import python.build.output_io as oio
import python.build.common as common


purchases = oio.readStage( common.subsample, "purchases_2_vat." + common.vat_strategy_suffix )

if True: # sum purchases within person
  purchases["transactions"] = 1 # useful later, when it is summed
  purchase_sums = purchases.groupby( ["household", "household-member"]
           ) [ "value"
             , "transactions"
             , "vat paid, max"
             , "vat paid, min"
           ] . agg("sum")
  purchase_sums = purchase_sums.reset_index( level = ["household", "household-member"] )

  oio.saveStage( common.subsample, purchase_sums, "purchase_sums." + common.vat_strategy_suffix )
