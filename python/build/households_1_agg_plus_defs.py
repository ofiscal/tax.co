if True:
  import python.common.common as c
  if c.regime_year == 2016:
    import python.regime.r2016 as regime
  else: import python.regime.r2018 as regime


# These do not vary within household.
cols_const_within_hh = ["region-1", "region-2", "estrato", "weight"]

# These are most of the columns that will be in the household data.
cols_most = ( [ "members"
              , "tax, ss, pension"
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
              , "income, rank 1"
              , "income, rank 2"
              , "income, rank 3"
              , "income, rank 4"
              , "income, rank 5"
              , "income, labor, rank 1"
              , "income, labor, rank 2"
              , "income, labor, rank 3"
              , "income, labor, rank 4"
              , "income, labor, rank 5"
              ] )

cols_to_min_or_max = [
     "age", "literate", "student", "female", "female head", "education"
    , "race, indig", "race, git|rom", "race, raizal", "race, palenq", "race, whi|mest"
    , "pension, receiving"
    , "pension, contributing (if not pensioned)"
    , "pension, contributor(s) (if not pensioned) = split"
    , "pension, contributor(s) (if not pensioned) = self"
    , "pension, contributor(s) (if not pensioned) = employer"
    , "seguro de riesgos laborales" ]
