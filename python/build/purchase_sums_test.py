# Beyond the shape of the data, there's nothing to test.

if True:
  import pandas as pd
  #
  import python.build.classes as cla
  import python.build.output_io as oio
  import python.common.common as com
  from   python.common.misc import num_households
  import python.common.util as util


sums = oio.readStage(
    com.subsample,
    "purchase_sums." + com.strategy_suffix )

assert util.unique( sums.columns )
assert ( set( sums.columns )  ==
         { "household",
           "value, tax, purchaselike non-VAT",
           "value, tax, predial",
           "value, tax, purchaselike non-predial non-VAT",
           "transactions",
           "value, non-purchase",
           "value, purchase",
           "value, spending",
           "value, consumption",
           "vat paid" } )

if com.subsample < 11: # The data is too sparse to test
                       # the smaller samples this way
  for (c,ts) in [
    ( "transactions",
      [ cla.MeanBounds    ( 50 , 120 ),
        cla.CoversRange   ( 2  , 200 ),
        cla.InRange       ( 1  , 400 ),
        cla.MissingAtMost ( 0 ) ] ),

    ( "value, tax, purchaselike non-VAT",
      [ cla.MeanBounds    (1e4 , 1e5),
        cla.CoversRange   (0   , 2e6),
        cla.InRange       (0   , 1.1e8), # someone pays a huge predial
        cla.MissingAtMost (0) ] ),

    ( "value, tax, predial",
      [ cla.MeanBounds    (1e4 ,1e5),
        cla.CoversRange   (0   ,1e3),
        cla.InRange       (0   ,1.1e8),
        cla.MissingAtMost (0) ] ),

    ( "value, tax, purchaselike non-predial non-VAT",
      [ cla.MeanBounds    (1e3 ,2e4),
        cla.CoversRange   (0 ,9e5),
        cla.InRange       (0 ,5e7), # surprising, given the range of the predial -- I would have imagined no other tax comes close
        cla.MissingAtMost (0) ] ),

     ( "value, non-purchase",
       [ cla.MeanBounds    (1e6,1e7),
         cla.CoversRange   (0 ,1e6),
         cla.InRange       (0 ,3.3e9),
         cla.MissingAtMost (0) ] ),

    ( "value, purchase",
       [ cla.MeanBounds    (1e6 ,5e6),
         cla.CoversRange   (1e2 ,4e7), # TODO ? This minimum is nuts.
         cla.InRange       (0   ,2e8),
         cla.MissingAtMost (0) ] ),

    ( "value, spending",
       [ cla.MeanBounds    (1e6 ,5e6),
         cla.CoversRange   (1e2 ,4e7), # TODO ? This minimum is nuts.
         cla.InRange       (0   ,2e8),
         cla.MissingAtMost(0) ] ) ]:
      for t in ts:
          assert t.test( sums[c] )

assert sums["household"].is_unique

assert util.near( len(sums),
                  num_households / com.subsample,
                  tol_frac = 1/5 )

oio.test_write( com.subsample,
                "build_purchase_sums",
                "It worked." )
