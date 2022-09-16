if True:
  from itertools import chain
  import python.common.common    as com
  if   com.regime_year == 2016:
      import python.regime.r2016 as regime
  elif com.regime_year == 2018:
      import python.regime.r2018 as regime
  else:
      import python.regime.r2019 as regime


def maybeFill(groupVar, val):
  if groupVar == "income-percentile":
    return val.zfill(2)
  else: return val

decile_names = { "income-decile: " + str(i)
                 : "[" + str(10*i) + "," + str(10*(i+1)) + ")"
                 for i in range(10) }

percentile_names = { "income-percentile: " + ( str(i) . zfill(2) )
                     : "[" + str(i) + "," + str(i+1) + ")"
                     for i in range(100) }

millile_names = { "income-millile: " + str(i) . zfill(3)
                  : "[" + str(i/10) + "," + str((i+1)/10) + ")"
                  for i in range(1000) }

quantileNames = { ** decile_names,
                  ** percentile_names,
                  ** millile_names }

householdGroupVars = [
  # Variables to group by, and optionally,
  # the subset of values for that group variable to consider.
  # If `None` then all values are considered.
  ( "one"                         , None ),
  ( "female head"                 , None ),
  ( "income-decile"               , None ),
  ( "income-percentile"           , None ),
  ( "income-millile"              , list ( range(990,1000) ) ),
  ( "income-percentile-in[90,97]" , [1]  ),
  ( "income-percentile-in[90,98]" , [1]  ),
  ( "income-millile-in[990,997]"  , [1]  ),
  ( "income-millile-in[990,998]"  , [1]  ),
  ( "region-2"                    , None ),
  ]

earnerGroupVars = (
  # The female/male distinction doesn't make sense at the household level
  # -- most households have both.
  # By contrast, "female head" does make sense at the earner level,
  # as it indicates whether someone lives in a household with a female head.
  # (Whether that's useful is a separate question.)
  [ ( "female", None ) ]
  + householdGroupVars )

#
# Variables to summarize
#

commonVars = ( [
  "female head",
  "income < min wage",
  "pension, receiving",
  # "pension, contributing (if not pensioned)",
  # "pension, contributor(s) (if not pensioned) = split",
  # "pension, contributor(s) (if not pensioned) = self",
  # "pension, contributor(s) (if not pensioned) = employer",
  # "seguro de riesgos laborales",
  "income - tax",
  "income",
  "tax",
  "income tax rate",
  "income, labor",
  "income, labor + cesantia",
  "income, rental + interest",
  "income, capital",
  "income, dividend",
  "income, pension",
  "income, govt",
  "income, private",
  "income, infrequent",
  "female head",
  "value, purchase",
  "purchase value / income",
  "vat paid",
  "vat / income",
  "vat / purchase value",
  "value, tax, predial",
  ] + regime.income_tax_columns + [
    "tax, ss",
    "tax, ss, pension",
    "tax, ss, pension, employer",
    "tax, ss, salud",
    "tax, ss, salud, employer",
    "tax, ss, solidaridad",
    "tax, ss, parafiscales",
    "tax, ss, cajas de compensacion",
    "cesantias + primas",
  ] )

householdSpecificVars = [
  "(rank, labor income) = 1",
  "(rank, labor income) = 2",
  "(rank, labor income) = 3",
  "(rank, labor income) = 4",
  "(rank, labor income) = 5",
  "members",
  ]

earnerSpecificVars = [
  "female",
]

householdVars = commonVars + householdSpecificVars
earnerVars    = commonVars + earnerSpecificVars


#
# Restricted sets of variables to summarize, for the simpler data frames
#

ofMostInterestLately = [
  "income tax sums / total income sums",
  "income: max",

  "income - tax: sums",
  "income - tax: mean",
  "income: sums",
  "income: mean",
  "tax: sums",
  "tax: mean",
  "income tax rate: mean",
  "income, labor: sums",
  "income, labor: mean",
  "income, labor + cesantia: sums",
  "income, labor + cesantia: mean",
  "tax, income: sums",
  "tax, income: mean",
  "tax, income: min",
  "tax, income: max",
  "tax, income, labor: sums",
  "tax, income, labor: mean",
  "tax, income, labor: min",
  "tax, income, labor: max",
  ]

commonRestrictedVars = ( [
  #####################
  # What we want lately
  #####################
  "income - tax: sums",
  "income - tax: mean",
  "income - tax: min",
  "income - tax: max",
  "income tax rate: mean",
  "income tax rate: min",
  "income tax rate: max",
  "income: mean",
  "income: min",
  "income: max",
  "income: sums",
  "tax: mean",
  "tax: min",
  "tax: max",
  "tax: sums",

  ######################################
  # The rest are of less interest lately
  ######################################
  "income < min wage: mean",
  "pension, receiving: mean",
  "pension, receiving: min",
  "pension, receiving: max",
  # "pension, contributing (if not pensioned): mean",
  # "pension, contributing (if not pensioned): min",
  # "pension, contributing (if not pensioned): max",
  # "pension, contributor(s) (if not pensioned) = split: mean",
  # "pension, contributor(s) (if not pensioned) = split: min",
  # "pension, contributor(s) (if not pensioned) = split: max",
  # "pension, contributor(s) (if not pensioned) = self: mean",
  # "pension, contributor(s) (if not pensioned) = self: min",
  # "pension, contributor(s) (if not pensioned) = self: max",
  # "pension, contributor(s) (if not pensioned) = employer: mean",
  # "pension, contributor(s) (if not pensioned) = employer: min",
  # "pension, contributor(s) (if not pensioned) = employer: max",
  # "seguro de riesgos laborales: mean",
  # "seguro de riesgos laborales: min",
  # "seguro de riesgos laborales: max",
  "income, labor: mean",
  "income, labor + cesantia: mean",
  "income, rental + interest: mean",
  "income, capital: mean",
  "income, dividend: mean",
  "income, dividend: share",
  "income, pension: mean",
  "income, govt: mean",
  "income, private: mean",
  "income, infrequent: mean",
  "female head: mean",
  "value, purchase: median_unweighted",
  "value, purchase: mean",
  "vat paid: mean",
  "vat paid: sums",
  "tax, income: sums",
  "tax, income, most: sums",
  "tax, income, dividend: sums",
  "tax, income, ganancia ocasional: sums",
  "tax, income, gmf: sums",
  "tax, ss, pension: sums",
  "tax, ss, salud: sums",
  "tax, ss, solidaridad: sums",
  "tax, ss, parafiscales: sums",
  "purchase value / income: median_unweighted",
  "purchase value / income: mean",
  "vat / purchase value: median_unweighted",
  "vat / purchase value: mean",
  "vat / income: median_unweighted",
  "vat / income: mean",
  "value, tax, predial: median_unweighted",
  "value, tax, predial: mean",
  ]

  # "chain.from_iterable" concatenates lists
  + list( chain.from_iterable( [ [ c + ": median_unweighted"
                                 , c + ": mean" ]
                                 for c in regime.income_tax_columns ] ) )
  + [
    "tax, ss, pension: median_unweighted",
    "tax, ss, pension: mean",
    "tax, ss, pension, employer: median_unweighted",
    "tax, ss, pension, employer: mean",
    "tax, ss, salud: median_unweighted",
    "tax, ss, salud: mean",
    "tax, ss, salud, employer: median_unweighted",
    "tax, ss, salud, employer: mean",
    "tax, ss, solidaridad: median_unweighted",
    "tax, ss, solidaridad: mean",
    "tax, ss, parafiscales: median_unweighted",
    "tax, ss, parafiscales: mean",
    "tax, ss, cajas de compensacion: median_unweighted",
    "tax, ss, cajas de compensacion: mean",
    "cesantias + primas: median_unweighted",
    "cesantias + primas: mean",
    "tax, income, gmf: median_unweighted",
    "tax, income, gmf: mean",
    "tax, income, ganancia ocasional: median_unweighted",
    "tax, income, ganancia ocasional: mean",
  ] )

householdSpecificRestrictedVars = [
  "(rank, labor income) = 1: mean",
  "(rank, labor income) = 1: mean_nonzero",
  "(rank, labor income) = 2: mean",
  "(rank, labor income) = 2: mean_nonzero",
  "(rank, labor income) = 3: mean",
  "(rank, labor income) = 3: mean_nonzero",
  "(rank, labor income) = 4: mean",
  "(rank, labor income) = 4: mean_nonzero",
  "(rank, labor income) = 5: mean",
  "(rank, labor income) = 5: mean_nonzero",
  "members: mean",
  ]

householdRestrictedVars = commonRestrictedVars + householdSpecificRestrictedVars
earnerRestrictedVars    = commonRestrictedVars + earnerSpecificVars
