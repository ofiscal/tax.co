# Aggregate purchases within person.

import python.build.output_io as oio
import python.common.common as c


purchases = oio.readStage( c.subsample
                         , "purchases_2_vat." + c.strategy_suffix )

# extract the predial tax
purchases["predial"] = (purchases["coicop"] == 12700601) * purchases["value"]
  # PITFALL: This variable, which is already part of the ENPH,
  # encodes not the value of the property, just the predial tax paid on the house.
  # It's confusing, because it comes from the purchase-level data, 
  # so you might reasonably expecet it to encode a purchase, not a tax.
  # "Impuesto predial y de valorización de la(s) vivienda(s) ocupada(s) por el hogar"
  # The coicop-vat bridge assigns that coicop code a vat of zero.

purchases["transactions"] = 1 # next this is summed within persons
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
