# Aggregate purchases within person.

import python.build.output_io as oio
import python.common.common as c


purchases = oio.readStage( c.subsample
                         , "purchases_2_vat." + c.strategy_suffix )

# extract the predial tax
purchases["predial"] = (purchases["coicop"] == 12700601) * purchases["value"]
  # This encodes not the value of the property, just the predial tax paid on the house.
  # "Impuesto predial y de valorización de la(s) vivienda(s) ocupada(s) por el hogar"
  # The coicop-vat bridge assigns it a vat of zero.

purchases["transactions"] = 1 # useful when summed
purchase_sums = purchases.groupby( ["household", "household-member"]
         ) [ "value"
           , "value, vat 0"
           , "value, vat 5"
           , "value, vat 19"
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
