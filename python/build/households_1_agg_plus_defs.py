if True:
  import python.common.common as c

  # PITFALL: Generates harmless mypy errors.
  # mypy assumes each import statement executes,
  # and therefore complains, `Name "regime" already defined`.
  if   c.regime_year == 2016:
      import python.regime.r2016 as regime
  elif c.regime_year == 2018:
      import python.regime.r2018 as regime
  else:
      import python.regime.r2019 as regime


# These do not vary within household.
cols_const_within_hh = ["region-1", "region-2", "estrato", "weight"]

# These are most of the columns that will be in the household data.
# They are aggregated through summation.
#
# PITFALL: This does not include the aggregate income variables like
# "IC" and "IT" that eventually appeared in the ENPH, because
# those (drawn from Viviendas, not Personas) are at the household level,
# not the individual level.
income_and_tax__person_level = ( [
    "tax, ss"
  , "tax, ss, pension"
  , "tax, ss, pension, employer"
  , "tax, ss, salud"
  , "tax, ss, salud, employer"
  , "tax, ss, solidaridad"
  , "tax, ss, parafiscales"
  , "tax, ss, cajas de compensacion"
  , "cesantias + primas" ]

  + regime.income_tax_columns +
  [ "income"
  , "income, cash"
  , "income, in-kind"
  , "income, capital"
  , "income, pension"
  , "income, cesantia"
  , "income, dividend"
  , "income, rental + interest"
  , "income, infrequent"
  , "income, govt"
  , "income, private"
  , "income, labor"
  , "income, borrowing"
  , "income, non-labor (tax def)"
  ] )

income_and_spending__household_level = [
  # PITFALL: Although these are peso-denominated, they are constant within household,
  # hence included here rather than in the list `income_and_tax__person_level`.
   "IT"
  ,"IC"
  ,"ICM"
  ,"ICMD"
  ,"GT"
  ,"GC"
  ,"GCM"
  ]

cols_income_rank = [ "(rank, labor income) = 1"
                   , "(rank, labor income) = 2"
                   , "(rank, labor income) = 3"
                   , "(rank, labor income) = 4"
                   , "(rank, labor income) = 5" ]

# These columns are aggregated via max and renamed.
# (Two of them, age and female, are also aggregated via min,
# but where that happens they are named individually.)
cols_to_max__pre_rename = (
    [ "age", "literate", "student", "female", "edu"
    , "race, indig", "race, git|rom", "race, raizal", "race, palenq", "race, whi|mest" ]
    )

# These columns are aggregated via max,
# but they retain the same name.
cols_to_max__no_name_change = [
    "used savings" # PITFALL: Varies within household.
  , "recently bought this house"
  , "female head"
  , "pension, receiving"
  , "pension, contributing (if not pensioned)"
  , "pension, contributor(s) (if not pensioned) = split"
  , "pension, contributor(s) (if not pensioned) = self"
  , "pension, contributor(s) (if not pensioned) = employer"
  , "seguro de riesgos laborales" ]

cols_to_max = ( cols_to_max__pre_rename
               + cols_to_max__no_name_change )

# The variables in cols_to_max__pre_rename, after aggregation,
# are renamed as these variables. Note that `cols_to_max__pre_rename`
# is smaller than `cols_to_max__post_rename`,
# because some things in the former (e.g. "female") become multiple things
# in the latter (e.g. "has-female" and "has-male").
cols_to_max__post_rename = (
    [ "age-min", # computed via agg(min)
      "has-male" ] +

    [ "age-max", # computed via agg(max)
      "has-lit",
      "has-student",
      "edu-max",
      "has-female",
      "has-indig",
      "has-git|rom",
      "has-raizal",
      "has-palenq",
      "has-whi|mest" ]
)

cols_new = (
    [ "(rank, labor income) = " + str(n) for n in range(1,6) ] +

    [ "members",
      "members in labor force",
      "adults",
      "has-child",
      "has-elderly",
      "all-elderly",
      "income-decile",
      "income-percentile",
      "income-millile",
      "one" ]
)

cols_all = ( ["household", "income tax rate"]
           + cols_const_within_hh
           + income_and_tax__person_level
           + income_and_spending__household_level
           + cols_to_max__no_name_change
           + cols_to_max__post_rename
           + cols_new
)
