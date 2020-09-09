exec( open( "tax-proposal/2020-08-21/build.py" ) . read() )

from python.common.util import near
import numpy as np
import weightedcalcs as weightLib
wc = weightLib.Calculator('weight')


# `qs` is a quantile- (specifically percentile-) level data frame.
qs = pd.DataFrame( {"income q" : np.arange( 0, 1, 0.01 ) } )
qs["income"] = ( qs["income q"] .
                 apply( lambda q:
                   wc.quantile( hh, "income", q ) ) )
qs = pd.concat( [qs
               , pd.DataFrame(
                   data = { "income": [np.inf]
                          , "income q" : [1] },
                   index = [100]
                   ) ] )
qs["income q"] = ( qs["income q"] .
                   apply( lambda x: round(100 * x) ) )
qs = qs["income"]

if True:
  def income_quantiles( incomes, thresholds ):
      q = 0
      acc = incomes.copy()
      for i in range(0, len(incomes)):
          if q < thresholds.index.max():
              if incomes.iloc[i] >= thresholds.loc[q+1]:
                  q = q+1
          acc.iloc[i] = q
      return acc
  test = income_quantiles(
      pd.Series( [0,1,2,3,4,5,6,7] ),
      pd.Series( [0,2,5] ) )
  assert (test == pd.Series([0,0,1,1,1,2,2,2])) . all()

hh = hh.sort_values("income")
hh["income q"] = income_quantiles(
    hh["income"], qs )
hh[["income", "income q"]]

( hh
  [ hh["income"] == 0 ]
  [["income", "income, labor", "income, pension",
    "tax, income, most", "tax, income, most, proposed"
    ]] .
  describe() .
  transpose() )

for stat in ["mean", "median"]:
  aggs = ( hh .
    groupby( "income q" ) .
    agg( { "income"                                    : stat,
           "tax"                                       : stat,
           "tax, proposed"                             : stat,
           "tax, income"                               : stat,
           "tax, income, proposed"                     : stat,
           "tax, income, most"                         : stat,
           "tax, income, most, proposed"               : stat,
           "tax, income, dividend"                     : stat,
           "tax, income, dividend, proposed"           : stat,

           "tax, income, ganancia ocasional"           : stat,
           # PITFALL : omits inheritance
           "tax, income, ganancia ocasional, proposed" : stat,
           "tax, income, inheritance, proposed"        : stat,

           "tax, income, gmf"                          : stat,
           "value, tax, purchaselike non-VAT"          : stat,
           "tax, ss"                                   : stat,
           } ) )

  aggs[[ "tax, income"
       , "tax, income, proposed"]]
  aggs[[ "tax, income, most"
       , "tax, income, most, proposed" ]]
  aggs[[ "tax, income, dividend"
       , "tax, income, dividend, proposed" ]]

  aggs[["tax, income, ganancia ocasional",
           # PITFALL : omits inheritance
        "tax, income, ganancia ocasional, proposed",
        "tax, income, inheritance, proposed"        ]]

  output = aggs.copy()
  output["income %ile"] = aggs.index.astype(int)
  output = (
    output[[
        "income %ile"
      , "income"
      , "tax, income"
      , "tax, income, proposed"
      , "tax, income, most"
      , "tax, income, most, proposed"
      , "tax, income, ganancia ocasional"
      , "tax, income, ganancia ocasional, proposed"
      , "tax, income, inheritance, proposed"
      , "tax, income, dividend"
      , "tax, income, dividend, proposed" ]]
    . rename( columns =
      { "tax, income"                               : "total"
      , "tax, income, proposed"                     : "total, prop"
      , "tax, income, most"                         : "most"
      , "tax, income, most, proposed"               : "most, prop"
      , "tax, income, dividend"                     : "dividend"
      , "tax, income, dividend, proposed"           : "dividend, prop"
      , "tax, income, ganancia ocasional"           : "ganancia ocasional"
      , "tax, income, ganancia ocasional, proposed" : "ganancia ocasional, prop"
      , "tax, income, inheritance, proposed"        : "inheritance" } )
    . transpose()
    . applymap( round ) # round every cell to the nearest integer
    )

  output.to_excel( "tax-2020." + stat + ".xlsx" )

if False:
  import matplotlib.pyplot as plt
  #
  def semilog_ratio( title, tax_base_name, function_name, function, xmin, xmax):
    x = np.arange(xmin, xmax, (xmax - xmin) / 10000)
    plt.semilogx( x,
                  [function(a) / a for a in x] )
    plt.ylabel('fraction of ' + tax_base_name + ' lost to tax')
    plt.xlabel(tax_base_name + ' in UVTs')
    plt.title(title)
  #
  def linear( title
            , tax_base_name
            , function_name
            , function
            , xmin
            , xmax
            ):
    x = np.arange(xmin, xmax, (xmax - xmin) / 10000)
    plt.plot( x,
              [function(a) for a in x] )
    plt.ylabel( "taxes (measured in UVTs)" )
    plt.xlabel(tax_base_name + ' in UVTs')
    plt.title(title)
