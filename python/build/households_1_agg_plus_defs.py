if True:
  import python.common.common as c
  if c.regime_year == 2016:
    import python.regime.r2016 as regime
  else: import python.regime.r2018 as regime


# These do not vary within household.
cols_const_within_hh = ["region-1", "region-2", "estrato", "weight"]

# These are most of the columns that will be in the household data.
# They are aggregated through summation.
income_and_tax = ( [ "tax, ss, pension"
              , "tax, ss, pension, employer"
              , "tax, ss, salud"
              , "tax, ss, salud, employer"
              , "tax, ss, solidaridad"
              , "tax, ss, parafiscales"
              , "tax, ss, cajas de compensacion"
              , "cesantias + primas"
              , "tax, gmf"
              , "tax, ganancia ocasional" ]

              + regime.income_tax_columns +
              [ "income"
              , "income, pension"
              , "income, cesantia"
              , "income, dividend"
              , "income, capital (tax def)"
              , "income, infrequent"
              , "income, govt"
              , "income, private"
              , "income, labor"
              , "income, borrowing"
              ] )

cols_income_rank = [ "income, rank 1"
                   , "income, rank 2"
                   , "income, rank 3"
                   , "income, rank 4"
                   , "income, rank 5"
                   , "income, labor, rank 1"
                   , "income, labor, rank 2"
                   , "income, labor, rank 3"
                   , "income, labor, rank 4"
                   , "income, labor, rank 5" ]


# These columns are aggregated through min or max (or both, in some cases),
# and renamed.
cols_to_min_or_max__pre_rename = [
     "age", "literate", "student", "female", "education"
    , "race, indig", "race, git|rom", "race, raizal", "race, palenq", "race, whi|mest" ]

# These columns are aggregated through min or max (or both, in some cases),
# but they retain the same name.
cols_to_min_or_max__no_name_change = [
      "female head"
    , "pension, receiving"
    , "pension, contributing (if not pensioned)"
    , "pension, contributor(s) (if not pensioned) = split"
    , "pension, contributor(s) (if not pensioned) = self"
    , "pension, contributor(s) (if not pensioned) = employer"
    , "seguro de riesgos laborales" ]

cols_to_min_or_max = ( cols_to_min_or_max__pre_rename
                     + cols_to_min_or_max__no_name_change )

# The variables in cols_to_min_or_max__pre_rename, after aggregation,
# are renamed as these variables. Note that `cols_to_min_or_max__pre_rename`
# is smaller than `cols_to_min_or_max__post_rename`,
# because some things in the former (e.g. "female") become multiple things
# in the latter (e.g. "has-female" and "has-male").
cols_to_min_or_max__post_rename = (
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
    [ "income, rank "        + str(n) for n in range(1,6) ] +
    [ "income, labor, rank " + str(n) for n in range(1,6) ] +

    [ "members", # computed ad-hoc
      "has-child",
      "has-elderly",
      "income-decile",
      "income-percentile",
      "one" ]
)

cols_all = ( ["household"]
           + cols_const_within_hh
           + income_and_tax
           + cols_to_min_or_max__no_name_change
           + cols_to_min_or_max__post_rename
           + cols_new
)

