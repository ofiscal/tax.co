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

groupVars = [ # Variables to group by, and optionally,
              # the subset of values for that group variable to consider.
              # If `None` then all values are considered.
  ( "one"                         , None ),
  ( "female head"                 , None ),
  ( "income-decile"               , None ),
  ( "income-percentile"           , None ),
  ( "income-percentile-in[90,97]" , [1]  ),
  ( "income-millile"              , list ( range(990,1000) ) ),
  ( "region-2"                    , None ),
  ]

#
# Variables to summarize
#

commonVars = ( [
  "income < min wage",
  "pension, receiving",
  # "pension, contributing (if not pensioned)",
  # "pension, contributor(s) (if not pensioned) = split",
  # "pension, contributor(s) (if not pensioned) = self",
  # "pension, contributor(s) (if not pensioned) = employer",
  # "seguro de riesgos laborales",
  "income",
  "tax",
  "income tax rate",
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

householdVars = commonVars + householdSpecificVars
earnerVars    = commonVars


#
# Restricted sets of variables to summarize, for the simpler data frames
#

ofMostInterestLately = [
  "income tax sums / total income sums",
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

  "tax, income, ganancia ocasional: sums",
  "tax, income, ganancia ocasional: mean",
  "tax, income, ganancia ocasional: min",
  "tax, income, ganancia ocasional: max",
  "tax, income: sums",
  "tax, income: mean",
  "tax, income: min",
  "tax, income: max",
  "tax, income, most: sums",
  "tax, income, most: mean",
  "tax, income, most: min",
  "tax, income, most: max",
  "tax, income, dividend: sums",
  "tax, income, dividend: mean",
  "tax, income, dividend: min",
  "tax, income, dividend: max",
  "tax, income, gmf: sums",
  "tax, income, gmf: mean",
  "tax, income, gmf: min",
  "tax, income, gmf: max",
  "tax, ss: sums",
  "tax, ss: mean",
  "tax, ss: min",
  "tax, ss: max",
  "income, labor + cesantia: sums",
  "income, labor + cesantia: mean",
  "income, labor + cesantia: min",
  "income, labor + cesantia: max",
  "income, rental + interest: sums",
  "income, rental + interest: mean",
  "income, rental + interest: min",
  "income, rental + interest: max",
  "income, capital: sums",
  "income, capital: mean",
  "income, capital: min",
  "income, capital: max",
  "income, dividend: sums",
  "income, dividend: mean",
  "income, dividend: min",
  "income, dividend: max",
  "income, pension: sums",
  "income, pension: mean",
  "income, pension: min",
  "income, pension: max",
  "income, govt: sums",
  "income, govt: mean",
  "income, govt: min",
  "income, govt: max",
  "income, private: sums",
  "income, private: mean",
  "income, private: min",
  "income, private: max",
  "income, infrequent: sums",
  "income, infrequent: mean",
  "income, infrequent: min",
  "income, infrequent: max",
  ]

commonRestrictedVars = ( [
  #####################
  # What we want lately
  #####################
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
earnerRestrictedVars    = commonRestrictedVars
