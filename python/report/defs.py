# PURPOSE:
# This defines the columns we report on in var_summaries_by_group.py,
# and how we group them.
# The group variables are columns of the generated reports.
# The other variables correspond to rows of it.
# Both sets depend on the report in question.

if True:
  from itertools import chain
  from typing import Dict, List, Set, Tuple, Optional, TypeVar
  from typing_extensions import TypeAlias
  import python.common.common    as com
  if   com.regime_year == 2016:
      import python.regime.r2016 as regime
  elif com.regime_year == 2018:
      import python.regime.r2018 as regime
  else:
      import python.regime.r2019 as regime


ColumnType = TypeVar("ColumnType")
GroupSpec : TypeAlias = (
  Tuple [ str, # the name of the column identifying the grouping variable
          Optional [
            # If present, this list specifies the values to use as groups.
            # If absent, all possible groups are generated.
            List [ ColumnType ] ] ] )

def fill_if_percentile (
    groupVar : str, # a column name
    val      : str, # Maybe numeric. Gets "transformed"
                    # (but this is a pure function).
)           -> str: # If `val` is a percentile, adds leading zeros to `val`.
  if groupVar[-10:] == "percentile":
    return val.zfill(2)
  else: return val

def decile_names (
    underlying_var_name : str # e.g. "income" or "IT"
) -> Dict [ str, str ]:
  return { underlying_var_name  +"-decile: " + str(i)
           : "[" + str(10*i) + "," + str(10*(i+1)) + ")"
           for i in range(10) }

def percentile_names (
    underlying_var_name : str # e.g. "income" or "IT"
) -> Dict [ str, str ]:
  return { underlying_var_name + "-percentile: " + ( str(i) . zfill(2) )
           : "[" + str(i) + "," + str(i+1) + ")"
           for i in range(100) }

def millile_names (
    underlying_var_name : str # e.g. "income" or "IT"
) -> Dict [ str, str ]:
  return { underlying_var_name + "-millile: " + str(i) . zfill(3)
           : "[" + str(i/10) + "," + str((i+1)/10) + ")"
           for i in range(1000) }

def quantileNames (
    underlying_var_name : str # e.g. "income" or "IT"
) -> Dict [ str, str ]:
    return { ** decile_names     ( underlying_var_name ),
             ** percentile_names ( underlying_var_name ),
             ** millile_names    ( underlying_var_name ) }

def quantile_group_vars (
    quantile_var : str # The underlying variable from which the quantiles were defined.
) -> List [ GroupSpec ]:
  return [
    ( quantile_var + "-decile"               , None ),
    ( quantile_var + "-percentile"           , None ),
    ( quantile_var + "-millile"              , list ( range(990,1000) ) ),
    ( quantile_var + "-percentile-in[90,97]" , [1]  ),
    ( quantile_var + "-percentile-in[90,98]" , [1]  ),
    ( quantile_var + "-millile-in[990,997]"  , [1]  ),
    ( quantile_var + "-millile-in[990,998]"  , [1]  ),
  ]

commonGroupVars : List [ GroupSpec ] = [
  ( "one"         , None ),
  ( "female head" , None ),
  ( "region-2"    , None ), ]

def householdGroupVars (
    income_var_for_quantiles : str
) -> List [ GroupSpec ]:
  return ( commonGroupVars
           + quantile_group_vars ( income_var_for_quantiles )
          )

def earnerGroupVars (
    income_var_for_quantiles : str
) -> List [ GroupSpec ]:
  return ( commonGroupVars
           + [ ( "female", None ) ]
           + quantile_group_vars ( income_var_for_quantiles ) )


#
# Variables to summarize
#

commonVars = ( [ # vars in both household- and earner-level data sets
  "female head",
  "female head",
  "income, capital",
  "income, dividend",
  "income, govt",
  "income, infrequent",
  "income, labor",
  "income, labor, cesantias + primas",
  "income, non-labor (tax def)",
  "income, pension",
  "income, private",
  "income, rental + interest",
  "pension, receiving",
  "tax",
  "tax, ss",
  "tax, ss, ARL",
  "tax, ss, ARL, employer",
  "tax, ss, aux transporte, employer",
  "tax, ss, cajas de compensacion",
  "tax, ss, parafiscales",
  "tax, ss, pension",
  "tax, ss, pension, employer",
  "tax, ss, salud",
  "tax, ss, salud, employer",
  "tax, ss, solidaridad",
  "value, purchase",
  "value, tax, predial",
  "vat / purchase value",
  "vat paid",
  # "pension, contributing (if not pensioned)",
  # "pension, contributor(s) (if not pensioned) = employer",
  # "pension, contributor(s) (if not pensioned) = self",
  # "pension, contributor(s) (if not pensioned) = split",
  # "seguro de riesgos laborales",
  ] + regime.income_tax_columns + [
  ] )

householdSpecificVars = [
  "(rank, labor income) = 1",
  "(rank, labor income) = 2",
  "(rank, labor income) = 3",
  "(rank, labor income) = 4",
  "(rank, labor income) = 5",
  "IT - tax",
  "IT < min wage",
  "income tax / IT",
  "IT",
  "IT per capita",
  "GT",
  "GT per capita",
  "members",
  "purchase value / IT",
  "purchase value / IT",
  "vat / IT",
  ]

earnerSpecificVars = [
  "female",
  "income - tax",
  "income < min wage",
  "income tax / income",
  "income",
  "purchase value / income",
  "vat / income",
]

householdVars = commonVars + householdSpecificVars
earnerVars    = commonVars + earnerSpecificVars


#
# Restricted sets of variables to summarize, for the simpler data frames
#

def ofMostInterestLately (
    total_income : str # a column name
) -> List [ str ]:
  return [
    total_income + " - tax: mean",
    total_income + " - tax: sums",
    "income tax sums / " + total_income + " sums",
    total_income + ": max",
    total_income + ": mean",
    total_income + ": sums",
    "income tax / "  + total_income,

    # The rest of these do not depend on `total_income`
    "income, labor: mean",
    "income, labor: sums",
    "tax, income, labor: max",
    "tax, income, labor: mean",
    "tax, income, labor: min",
    "tax, income, labor: sums",
    "tax, income: max",
    "tax, income: mean",
    "tax, income: min",
    "tax, income: sums",
    "tax: mean",
    "tax: sums",
  ]
