# Aggregate purchases within person.

import python.build.output_io as oio
import python.common.common as c


purchases = oio.readStage(
    c.subsample,
    "purchases_2_vat." + c.strategy_suffix )

if True: # deal with taxes encoded as purchases
  # PITFALL: The ENPH "purchase data" is not all purchases; some is taxes.
  # For instance, "predial_tax" below encodes not the value of the property,
  # just the tax paid on it.
  # The coicop-vat bridge assigns that coicop code a vat of zero.

  predial_tax = 12700601
  tax_coicops = { predial_tax,
                  12700602,  # vehiculo
                  12700603,  # renta
                  12700699 } # otros

  if True: # extract the predial tax into its own column
    # TODO ? Retain other taxes beyond predial?
    purchases["predial"] = (
        (purchases["coicop"] == predial_tax)
        * purchases["value"] )

purchases["value, purchase"] = (
    (purchases[ "is-purchase" ] > 0) *
    purchases["value"] )
purchases["value, non-purchase"] = (
    (purchases[ "is-purchase" ] == 0) *
    purchases["value"] )
lpurchases = purchases.drop(
    columns = "value" )

# To analyze time to save for a month,
# these should be kept.
#  if True: # discard any purchases that are really taxes
#    purchases = purchases[ ~ purchases["coicop"]
#                           . isin( tax_coicops ) ]

purchases["transactions"] = 1 # next this is summed within persons
purchase_sums = purchases.groupby( ["household"]
         ) [ "value, purchase"
           , "value, non-purchase"
           , "transactions"
           , "vat paid, max"
           , "vat paid, min"
           , "predial"
           , "home purchase value"
         ] . agg("sum")
purchase_sums = purchase_sums.reset_index(
  level = ["household"] )

oio.saveStage( c.subsample
             , purchase_sums
             , "purchase_sums." + c.strategy_suffix )

