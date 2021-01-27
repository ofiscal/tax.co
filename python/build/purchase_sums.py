# Aggregate purchases within person.

if True:
  import re as regex
  #
  import python.build.output_io as oio
  import python.common.common as c


purchases = oio.readStage(
    c.subsample,
    "purchases_2_vat." + c.strategy_suffix )

if True: # Deal with taxes encoded as purchases.
  # PITFALL: The ENPH "purchase data" is not all purchases; some is taxes.
  # For instance, "predial_tax" below encodes not the value of the property,
  # just the tax paid on it.
  # The coicop-vat bridge assigns that coicop code a vat of zero.
  #
  predial_tax = 12700601
  other_tax_coicops = { 12700602,  # vehiculo
                        12700603,  # renta
                        12700699 } # otros
  purchases["value, tax, predial"] = (
    (purchases["coicop"] == predial_tax)
    * purchases["value"] )
  purchases["value, tax, purchaselike non-predial non-VAT"] = ( # vehicle, rent, and "other" taxes
    (purchases["coicop"] . isin( other_tax_coicops ) )
    * purchases["value"] )
  #
  # Delete those taxes from the "value" column.
  other_tax_coicops.add( predial_tax )
  purchases.loc[
    purchases["coicop"] . isin( other_tax_coicops ),
    "value"] = 0

purchases["value, purchase"] = (
    (purchases[ "is-purchase" ] > 0) *
    purchases["value"] )
purchases["value, non-purchase"] = (
    (purchases[ "is-purchase" ] == 0) *
    purchases["value"] )
lpurchases = purchases.drop(
    columns = "value" )

if True: # VAT is only charged for purchases; zero it for other things.
    # TODO (speed) ? It would be more efficient if the vat calculations
    # being nullified here never happened to begin with.
    # (They happen in purchases_2_vat.py.)
  vat_regex = regex.compile( "^vat" )
  vat_columns = [ col for col in purchases.columns
                   if vat_regex.match( col ) ]
    # This could change -- that's why I use a regexp -- but currently,
    # vat_columns is equal to this:
    #   [ 'vat', 'vat, min', 'vat, max', 'vat frac', 'vat frac, min',
    #     'vat frac, max', 'vat paid, min', 'vat paid, max']
  #
  for col in vat_columns:
      purchases[col] = (
          (purchases[ "is-purchase" ] > 0) *
          purchases[col] )

purchases["transactions"] = 1 # next this is summed within persons
purchase_sums = purchases.groupby( ["household"]
         ) [ [ "value, purchase"
             , "value, non-purchase"
             , "transactions"
             , "vat paid, max"
             , "vat paid, min"
             , "value, tax, predial"
             , "value, tax, purchaselike non-predial non-VAT"
         ] ] . agg("sum")
purchase_sums = purchase_sums.reset_index(
  level = ["household"] )

if True: # It's faster to compute these columns post-aggregation.
  purchase_sums["value, tax, purchaselike non-VAT"] = (
        purchase_sums["value, tax, predial"] +
        purchase_sums["value, tax, purchaselike non-predial non-VAT"] )
  purchase_sums["value, spending"] = ( # Taxes and purchases, but no gifts.
      # PITFALL: Includes VAT (it's part of "value, purchase").
      purchase_sums["value, tax, purchaselike non-VAT"] +
      purchase_sums["value, purchase"] )

  purchase_sums["value, consumption"] = ( # purchases and gifts, but no taxes (except VAT)
      # PITFALL: Includes VAT (it's part of "value, purchase").
      purchase_sums["value, non-purchase"] +
      purchase_sums["value, purchase"] )

oio.saveStage( c.subsample
             , purchase_sums
             , "purchase_sums." + c.strategy_suffix )
