import sys

import python.vat.build.output_io as oio
import python.vat.build.legends as legends


subsample = int( sys.argv[1] ) # Reciprocal of subsample size. Valid: 1, 10, 100, 1000.


if True: # input files
  # This data set is too big unless I down-cast the numbers.
  purchases = oio.readStage( subsample
                           , "purchases_1_5_no_origin"
                           , dtype = {
                               "25-broad-categs" : "float32"
                             , "coicop" : "float32"
                             , "freq" : "float32"
                             , "household" : "int32"
                             , "household-member" : "int32"
                             , "is-purchase" : "float32"
                             , "quantity" : "float32"
                             , "value" : "float32"
                             , "weight" : "float32"
                             , "where-got" : "float32"
                           } )
  vat_cap_c = oio.readStage( subsample
                           , "vat_cap_c_brief"
                           , dtype = {
                             "25-broad-categs" : "int32"
                             , "vat" : "float32"
                             , "vat, min" : "float32"
                             , "vat, max" : "float32"
                             , "vat frac" : "float32"
                             , "vat frac, min" : "float32"
                             , "vat frac, max" : "float32"
                           } )
  vat_coicop = oio.readStage( subsample
                            , "vat_coicop_brief"
                            , dtype = {
                                "coicop" : "int32"
                              , "vat" : "float32"
                              , "vat, min" : "float32"
                              , "vat, max" : "float32"
                              , "vat frac" : "float32"
                              , "vat frac, min" : "float32"
                              , "vat frac, max" : "float32"
                            } )


if True: # add VAT to purchases
  purchases = purchases.merge( vat_coicop, how = "left", on="coicop" )
  purchases = purchases.merge( vat_cap_c, how = "left", on="25-broad-categs" )

  # Since vat_cap_c and vat_coicop have like-named columns, the second merge causes
  # a proliferation of like-named columns ending in _x or _y. The next section picks,
  # for each pair name_x and name_y, a master value for the name column, then discards
  # the two that were selected from.

  for (result, x, y) in [ ("vat", "vat_x","vat_y")
                        , ("vat frac", "vat frac_x","vat frac_y")
                        , ("vat frac, min", "vat frac, min_x","vat frac, min_y")
                        , ("vat frac, max", "vat frac, max_x","vat frac, max_y")
                        , ("vat, min", "vat, min_x","vat, min_y")
                        , ("vat, max", "vat, max_x","vat, max_y") ]:
    purchases.loc[ ~purchases[x].isnull(), result] = purchases[x]
    purchases.loc[  purchases[x].isnull(), result] = purchases[y]
    purchases = purchases.drop( columns = [x,y] )

  purchases["freq-code"] = purchases["freq"]
    # kept for the sake of drawing a table of purchase frequency
    # with frequencies spread evenly across the x-axis
  purchases["freq"].replace( legends.freq
                           , inplace=True )
  purchases = purchases.drop(
    purchases[ purchases["freq"].isnull() ]
    .index
  )

  purchases["value"] = purchases["freq"] * purchases["value"]
  purchases["vat paid, max"] = purchases["value"] * purchases["vat frac, max"]
  purchases["vat paid, min"] = purchases["value"] * purchases["vat frac, min"]

  oio.saveStage(subsample, purchases, 'purchases_2_vat')
