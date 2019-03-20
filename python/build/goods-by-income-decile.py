# Maria del Rosario Guerra asked us what would happen if we exempted the most
# common purchases by income decile. This computes the most common purchases
# per income decile.

import pandas as pd
import python.build.output_io as oio
import python.common.util as util
import python.common.misc as c
import python.common.cl_args as c


#class common:
#  subsample = 100

vat_aware = True # If true, this causes the code below to only find the most popular goods
  # among goods that are currently charged 0 (or up to 5%) vat but would carry 18% vat under
  # the proposal from 2018-10-31.


## ## ## ## ## Ingest data ## ## ## ## ##

# PITFALL: Always the detail vat strategy, because irrelevant.
hs = oio.readStage( c.subsample
                  , "households." + "detail_"
                  , usecols = ["household", "income-decile"]
)

ps = oio.readStage( c.subsample, 'purchases_1_5_no_origin'
                  , usecols = ["household", "value", "coicop"]
)
ps = ps[ ~ ps["coicop"] . isnull() ] # purchases coded by cap c, not coicop: discard
ps["coicop"] = util.pad_column_as_int( 8, ps["coicop"] )
ps["coicop-2-digit"] = ps["coicop"] . apply( lambda s: s[0:2] )
ps["coicop-3-digit"] = ps["coicop"] . apply( lambda s: s[0:3] )

tax_proposed_2_digit = pd.read_csv( "python/build/vat_prop_2018_10_31/2-digit.csv"
                                    , usecols = ["coicop-2-digit","vat"] )
if vat_aware:
  tax_proposed_2_digit = tax_proposed_2_digit[ tax_proposed_2_digit["vat"] > 0 ]

tax_proposed_2_digit["coicop-2-digit"] = (
  util.pad_column_as_int( 2, tax_proposed_2_digit["coicop-2-digit"] ) )

tax_proposed_3_digit = pd.read_csv( "python/build/vat_prop_2018_10_31/3-digit.csv"
                                    , usecols = ["coicop-3-digit","vat"] )
if vat_aware:
  tax_proposed_3_digit = tax_proposed_3_digit[ tax_proposed_3_digit["vat"] > 0 ]

tax_proposed_3_digit["coicop-3-digit"] = (
  util.pad_column_as_int( 3, tax_proposed_3_digit["coicop-3-digit"] ) )

currently_untaxed = pd.read_csv( "data/vat/vat-by-coicop.csv"
  , sep=";"
  , usecols = ["coicop", "vat, min", "description"] )
currently_untaxed["coicop"] = util.pad_column_as_int( 8, currently_untaxed["coicop"] )
if vat_aware:
  currently_untaxed = currently_untaxed[
                        currently_untaxed["vat, min"] <= 0.05 ]


## ## ## ## ## Isolate to the "vat-marginal" COICOP codes ## ## ## ## ##
# (that is, codes for which the current regime does not impose VAT while the proposal does)

ps_vat = ps.merge( currently_untaxed, how = "inner", on = "coicop" )
ps_2_digit = ps_vat.merge( tax_proposed_2_digit, how = "right"
                     , on="coicop-2-digit" )
ps_3_digit = ps_vat.merge( tax_proposed_3_digit, how = "right"
                     , on="coicop-3-digit" )
ps_vat = ps_2_digit . combine_first( ps_3_digit )
ps_vat = ps_vat.rename( columns = { "vat, min" : "vat, current min"
                                  , "vat" : "vat, proposed"
} )
ps_vat["vat, proposed"] = ps_vat["vat, proposed"] * 0.18


## ## ## ## ## Group by deciles ## ## ## ## ##

ps_all = ps_vat.merge( hs, on = "household" )

grouped = ps_all . groupby( ["income-decile","coicop"]
  ) . agg( { "value":"sum"
           , "vat, current min" : "first"
           , "vat, proposed" : "first"
           , "description" : "first"
  } ) . sort_values( "value"
                 , ascending = False
  ) . reset_index(
  ) . groupby( ["income-decile"]
  ) . head( 100
  ) . sort_values( ["income-decile","value"]
                 , ascending = [True,False]
)

grouped.to_csv( "output/vat/tables/recip-" + str(c.subsample) + "/goods_by_income_decile.csv" )


## ## ## ## ## The bottom 60% ## ## ## ## ##

ps_60 = ps_all[ ps_all["income-decile"] <= 5]

ps_60_grouped = ps_60 . groupby( "coicop"
  ) . agg( { "value":"sum"
       # , "description": "first" # PITFALL: disabled while Luis does by hand
  } ) . sort_values( "value"
                   , ascending = False
  ) . reset_index(
  ) . head( 100
  ) . sort_values( "value"
                 , ascending = False
)

ps_60_grouped = ps_60_grouped.merge(
  currently_untaxed[["coicop","description"]]
  , how = "left"
  , on = "coicop" )

grouped.to_csv( "output/vat/tables/recip-" + str(c.subsample) + "/goods,first_six_deciles.csv" )


# A test

if False: # TODO: HUnit
  for i in range(0, len(ps_60_grouped)):
    x = ( ps_all[ (ps_all["income-decile"] <= 5)
                      & (ps_all["coicop"] == ps_60_grouped.iloc[i]["coicop"])
                    ]["value"].sum()
            ) == ps_60_grouped.iloc[i]["value"]
    if not x: print( "TEST FAILED in goods-by-income-decile.py for i = " + str(i))
  del(x)
