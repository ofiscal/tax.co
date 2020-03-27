# This computes the fractions of personal labor and cesantias income
# in the informal and formal sectors, by assuming that anybody
# who makes less than the minimum wage is in the informal one.

if True:
  import pandas                 as pd
  #
  import python.build.output_io as oio
  from   python.common.misc     import min_wage
  import python.common.common   as cl


ppl = oio.readStage(
  cl.subsample,
  'people_4_income_taxish.' + cl.strategy_year_suffix
)

ppl["cash labor + cesantias"] = (
    ppl["income, labor, cash"] +
    ppl["income, cesantia"] )

for c in ["income, labor, cash", "cash labor + cesantias"]:
  total = ppl[c].sum()
  formal   = ( ppl[ ppl[c] >= min_wage ][c].sum() ) / total
  informal = ( ppl[ ppl[c] <  min_wage ][c].sum() ) / total
  print(c + ":")
  print("  formal: "   + str(formal) )
  print("  informal: " + str(informal) )

# I tested that with the following data.
# (It requires replacing min_wage with mw, and ppl with df, in the for loop.)
#   ppl["cash labor + cesantias"] = (
#       ppl["income, labor, cash"] +
#       ppl["income, cesantia"] )
#   df = pd.DataFrame( {
#       "income, labor, cash" : [0,4,8,12],
#       "cash labor + cesantias" : [2,6,10,14]
#     } )
#   mw = 11
# Expected output:
#   income, labor, cash:
#     formal: 0.5
#     informal: 0.5
#   cash labor + cesantias:
#     formal: 0.4375
#     informal: 0.5625
