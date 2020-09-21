# This processes individual columns from the person-level ENPH data.
# It's a long process, but not as complex as it looks,
# because the processing is very "flat" --
# most variables can be considered in isolation,
# as there are very few interconnections between them to worry about here.
# Most of the variables processed here are forms of income,
# of which the ENPH has around 75.
#
# TODO: divide into sub-modules

if True:
  import numpy as np
  import pandas as pd
  import re as regex
  #
  import python.build.classes as cla
  import python.build.output_io as oio
  import python.build.people.main_defs as defs
  import python.build.people.files as files
  import python.common.common as cl
  import python.common.misc as c


ppl = oio.readStage(cl.subsample, 'people_0')

ppl = ppl.drop( # drop non-members of household
  ppl[ ppl["relationship"].isin( [6,7,8] )
  ].index )

if True: # make independiente a 0 or a 1
  ppl["independiente"] = ppl[ "independiente"
                         ] . apply( lambda x: 1 if x in [4,5] else 0 )

if True: # remap some boolean integers
  for cn in ( [ "female" ] + # originally 1=male, 2=female
              [included for (_,included) in files.inclusion_pairs]
                 # originally, 1=included, 2=forgot
  ): ppl[cn] = ppl[cn] - 1
  #
  for cn in [ "student"         # originally 1=student, 2=not
            , "skipped 3 meals" # originally 1=yes, 2=no
            , "literate"        # originally 1=yes, 2=no
  ]: ppl[cn] = 2 - ppl[cn]

if True: # non-income characteristics: pension and labor insurance
  ppl["pension, contributing (if not pensioned)"] = (
    ppl["pension, contributing, pre"]
    . apply( lambda x:
             ( 1 if x==1
               else ( 0 if x==2
                      else np.nan ) ) ) )
  #
  ppl["pension, receiving"] = (
      ( ppl["pension, contributing, pre"] == 3 )
    | ( ppl["income, month : pension : age | illness"] > 0 )
  ) . astype('int')
  #
  ppl["pension, contributor(s) (if not pensioned) = split"] = (
    ppl["pension, contributors, pre"]
    . apply( lambda x: 1 if x == 1 else
             ( 0 if (x > 0) & (x < 4) else np.nan ) ) )
  #
  ppl["pension, contributor(s) (if not pensioned) = self"] = (
    ppl["pension, contributors, pre"]
    . apply( lambda x: 1 if x == 2 else
             ( 0 if (x > 0) & (x < 4) else np.nan ) ) )
  #
  ppl["pension, contributor(s) (if not pensioned) = employer"] = (
    ppl["pension, contributors, pre"]
    . apply( lambda x: 1 if x == 3 else
             ( 0 if (x > 0) & (x < 4) else np.nan ) ) )
  #
  ppl["seguro de riesgos laborales"] = (
    ppl["seguro de riesgos laborales, pre"]
    . apply( lambda x: 1 if x==1 else
             ( 0 if x==2 else np.nan ) ) )
  #
  ppl = ppl.drop( columns = [ "pension, contributing, pre"
                            , "pension, contributors, pre"
                            , "seguro de riesgos laborales, pre" ] )

if True: # income
  if True: # fill NaN values
    # For months, interpret NaN as "one"
    ppl[   "income, month : labor : independent, months" ] = (
      ppl[ "income, month : labor : independent, months" ] . fillna(1) )
    #
    # For pesos, interpret NaN, 98 and 99 as "zero".
    # TODO ? Create a new makefile target in which 98s and 99s are dropped.
    cols_from_na_98_99_to_0 = ( list( cla.name_map( files.income )
                               . values() )
                         + list( cla.name_map( files.beca_sources_private )
                               . values() )
                         + list( cla.name_map( files.beca_sources_govt )
                               . values() ) )
    ppl[cols_from_na_98_99_to_0] = ppl[cols_from_na_98_99_to_0] . fillna(0)
    for col in cols_from_na_98_99_to_0: # 98 and 99 are error codes for
                                   # "doesn't know" and "won't say"
      ppl[col] = ppl[col].apply(
        lambda x : 0 if ((x >= 98) & (x <= 99)) else x )
    del(cols_from_na_98_99_to_0)
    #
  if True: # divide yearly income variables by 12, and rename
    re_year_income  = regex.compile( "^income, year" )
    year_columns = [ col for col in ppl.columns
                     if re_year_income.match( col )]
    for col in year_columns:
      ppl[col] = ppl[col] / 12
    ppl = ppl.rename(
      columns = dict( zip( year_columns
                         , defs.rename_monthly( year_columns ) ) ) )
    #
  re_in_kind = regex.compile( "^income.*in.kind$" )
  #
  if True: # compute income totals, drop components
    if True: # divide educational income by source (government or private)
      ppl["non-beca sources"] = ppl["non-beca sources"] . apply( str )
        # because if none of the values included more than one source (true
        # in subsamples), it was by default interpreted as a number.
      #
      ppl["non-beca sources, govt"] = ppl["non-beca sources"
                                      ] . apply( defs.count_public )
      ppl["non-beca sources, private"] = ppl["non-beca sources"
                                         ] . apply( defs.count_private )
      ppl["non-beca sources, total"] = ( ppl["non-beca sources, govt"]
                                       + ppl["non-beca sources, private"] )
      #
      ppl["beca sources, govt"]    = (
        ppl[ list( cla.name_map( files.beca_sources_govt )
                 . values() )
           ] . sum( axis=1 ) )
      ppl["beca sources, private"] = (
        ppl[ list( cla.name_map( files.beca_sources_private )
                 . values() )
           ] . sum( axis=1 ) )
      ppl["beca sources, total"] = ( ppl["beca sources, govt"]
                                   + ppl["beca sources, private"] )
      #
      ppl[     "income, month : govt : beca, cash"] = 0
      ppl.loc[ ppl["beca sources, total"] > 0
             , "income, month : govt : beca, cash" ] = (
        ppl[   "income, month : edu : beca, cash"]
        * ppl["beca sources, govt"] / ppl["beca sources, total"] )
      #
      ppl[     "income, month : private : beca, cash"] = 0
      ppl.loc[ ppl["beca sources, total"] > 0
             , "income, month : private : beca, cash" ] = (
        ppl[   "income, month : edu : beca, cash"]
        * ppl["beca sources, private"] / ppl["beca sources, total"] )
      #
      ppl[     "income, month : govt : non-beca, cash"] = 0
      ppl.loc[ ppl["non-beca sources, total"] > 0
             , "income, month : govt : non-beca, cash"] = (
        ppl["income, month : edu : non-beca, cash"]
        * ppl["non-beca sources, govt"] / ppl["non-beca sources, total"] )
      #
      ppl[     "income, month : private : non-beca, cash"] = 0
      ppl.loc[ ppl["non-beca sources, total"] > 0
             , "income, month : private : non-beca, cash"] = (
        ppl["income, month : edu : non-beca, cash"]
        * ppl["non-beca sources, private"] / ppl["non-beca sources, total"] )
      #
      ppl[     "income, month : govt : beca, in-kind"] = 0
      ppl.loc[ ppl["beca sources, total"] > 0
             , "income, month : govt : beca, in-kind" ] = (
        ppl["income, month : edu : beca, in-kind"]
        * ppl["beca sources, govt"]     / ppl["beca sources, total"] )
      #
      ppl[     "income, month : private : beca, in-kind"] = 0
      ppl.loc[ ppl["beca sources, total"] > 0
             , "income, month : private : beca, in-kind" ] = (
        ppl["income, month : edu : beca, in-kind"]
        * ppl["beca sources, private"]  / ppl["beca sources, total"] )
      #
      ppl[     "income, month : govt : non-beca, in-kind"] = 0
      ppl.loc[ ppl["non-beca sources, total"] > 0
             , "income, month : govt : non-beca, in-kind"] = (
        ppl["income, month : edu : non-beca, in-kind"]
        * ppl["non-beca sources, govt"] / ppl["non-beca sources, total"] )
      #
      ppl[     "income, month : private : non-beca, in-kind"] = 0
      ppl.loc[ ppl["non-beca sources, total"] > 0
             , "income, month : private : non-beca, in-kind"] = (
        ppl["income, month : edu : non-beca, in-kind"]
        * ppl["non-beca sources, private"] / ppl["non-beca sources, total"] )
      #
      new_edu_income_variables = ppl.filter(
        regex = "^income, month : (govt|private) : (beca|non-beca)" )
      new_edu_income_variables = new_edu_income_variables.fillna(0)
      #
      del(new_edu_income_variables)
      ppl = (ppl
        ).drop( columns = ppl.filter( regex = "(beca source|beca from)"
                          ).columns
        ).rename( columns = {
              "income, month : edu : beca, in-kind"
            :        "income : edu : beca, in-kind"
          ,   "income, month : edu : non-beca, in-kind"
            :        "income : edu : non-beca, in-kind"
          ,   "income, month : edu : beca, cash"
            :        "income : edu : beca, cash"
          ,   "income, month : edu : non-beca, cash"
            :        "income : edu : non-beca, cash" } )
      #
    if True: # govt income (cash + in-kind)
      # TODO ? Should this include becas of govt origin?
      cols_govt = list( cla.name_map( files.income_govt )
                      . values() )
      cols_govt_cash    = [ col for col in defs.rename_monthly( cols_govt )
                            if not re_in_kind.match(col) ]
      cols_govt_in_kind = [ col for col in defs.rename_monthly( cols_govt )
                            if     re_in_kind.match(col) ]
      ppl["total income, monthly : govt, cash"] = (
        ppl[ cols_govt_cash ].sum( axis=1 ) )
      ppl["total income, monthly : govt, in-kind"] = (
        ppl[ cols_govt_in_kind ].sum( axis=1 ) )
      ppl = ppl.drop( columns = cols_govt_in_kind + cols_govt_cash )
      #
    if True: # income, non-labor (tax def) ("ingreso no laboral")
      ppl["income, sale not real estate"] = (
          ppl["income, month : sale : stock"]
        + ppl["income, month : sale : stock ?2"]
        + ppl["income, month : sale : livestock"]
        + ppl["income, month : sale : vehicle | equipment"] )
      #
      # PITFALL: The tax code defines non-labor income
      # to include edu income only if it is not from the government.
      ppl["income, non-labor (tax def)"] = (
          ppl["income, sale not real estate"]
        + ppl["income, month : private : beca, cash"]
        + ppl["income, month : private : beca, in-kind"] )
      #
      ppl["income, govt edu, cash"] = (
        ppl["income, month : govt : beca, cash"]     +
        ppl["income, month : govt : non-beca, cash"] )
      ppl["income, govt edu, in-kind"] = (
        ppl["income, month : govt : beca, in-kind"]  +
        ppl["income, month : govt : non-beca, in-kind"] )
      #
    if True: # capital income (which is never in-kind)
      ppl["income, rental + interest"] = (
          # PITFALL: `cols_capital` includes dividends, but this does not.
          ppl["income, month : investment : interest"]
        + ppl["income, month : rental : real estate, developed"]
        + ppl["income, month : rental : real estate, undeveloped"]
        + ppl["income, month : rental : vehicle | equipment"] )
      #
      cols_capital = [ "income, month : investment : dividends"
                     , "income, month : investment : interest"
                     , "income, month : rental : real estate, developed"
                     , "income, month : rental : real estate, undeveloped"
                     , "income, month : rental : vehicle | equipment" ]
      #
      # drop most components, but keep dividend income
      ppl = ppl.drop(
        columns = list( set ( cols_capital )
                      - set ( ["income, month : investment : dividends"] )
      ) )
      #
    if True: # private income (cash + in-kind)
      # TODO ? Should these include private beca sources?
      cols_private = defs.rename_monthly(
                       list( cla.name_map( files.income_private )
                           . values() ) )
      ppl["total income, monthly : private"] = (
        ppl[ cols_private ].sum( axis=1 ) )
      ppl["income, donacion"] = (
        # todo ? this is unused
        # PITFALL: overlaps what will be called "income, private"
        ppl["income, month : private : from private domestic ?firms"] +
        ppl["income, month : private : from private foreign ?firms"] )
      #
      ppl = ppl.drop( columns = cols_private )
      #
    if True: # infrequent income (cash only)
      cols_infrequent = defs.rename_monthly(
          list( cla.name_map( files.income_infrequent )
                . values() )
          + ["income, year : sale : real estate"] )
      #
      ppl["total income, monthly : infrequent"] = (
        ppl[ cols_infrequent ].sum( axis=1 ) )
      #
      ppl["income, ganancia ocasional, 10%-taxable"] = (
        # PITFALL: This is not all ganancia ocasional income,
        # only the portion that is taxable.
        # Rather than use this as a componnent of total income,
        # use "income, infrequent", which includes all of it
        # (both the 10%- and the 20%-taxable kinds).
        ppl["income, month : sale : real estate"] +
        # PITFALL: Inheritance is taxed separately under the 2020 proposal.
        # Currently that complication is handled by subtracting inheritance
        # from this downstream (in python.regime.r2019).
        ppl["income, month : infrequent : inheritance"] +
        ppl["income, donacion"].apply(
          lambda x: x - min ( x * 0.2
                            , c.muvt * 2290  ) ) )
      #
      ppl["income, ganancia ocasional, 20%-taxable"] = (
        ppl["income, month : infrequent : gambling"] +
        ppl["income, month : infrequent : jury awards"] )
      ppl = ppl.drop( columns =
                      set(cols_infrequent) -
                      set(["income, month : infrequent : inheritance"])
                      )
      #
    if True: # "income" from borrowing
      cols_borrowing = defs.rename_monthly(
                         list( cla.name_map( files.income_borrowing )
                             . values() ) )
      ppl["income, borrowing"] = (
        ppl[ cols_borrowing ].sum( axis=1 ) )
      #
    if True: # labor income
      if True: # normalize independent labor income to one months' worth
        s = "income, month : labor : independent"
        ppl[s] = ppl[s] * ppl[s + ", months"]
        ppl = ppl.drop( columns = [s + ", months"] )
        del(s)
        #
      if True: # Only after the following does it makes sense to
               # sum all labor income variables.
               # Otherwise we would double-count some things.
        for (quantity, wasOmitted) in files.inclusion_pairs:
          ppl[ quantity ] = ppl[ quantity ] * ppl[ wasOmitted ]
        ppl = ppl.drop(
          columns = [ wasOmitted for (_, wasOmitted) in files.inclusion_pairs ] )
        #
      if True: # Compute cash and in-kind labor income sums.
        cols_labor  = list( cla.name_map( files.income_labor )
                          . values() )
        cols_labor_cash    = [ col for col in cols_labor if not re_in_kind.match(col) ]
        cols_labor_in_kind = [ col for col in cols_labor if     re_in_kind.match(col) ]
        ppl["total income, monthly : labor, cash"] = (
          ppl[ defs.rename_monthly( cols_labor_cash ) ]
          . sum( axis=1 ) )
        ppl["total income, monthly : labor, in-kind"] = (
          ppl[ defs.rename_monthly( cols_labor_in_kind ) ]
          . sum( axis=1 ) )
        ppl = ppl.drop(
          columns = defs.rename_monthly(
            cols_labor_in_kind + cols_labor_cash ) )
        #
    if True: # homogenize, shorten income variable names
      income_short_name_dict_cash = {
          'income, month : pension : age | illness'  : "income, pension"
        , 'income, month : cesantia'                 : "income, cesantia"
        , "income, month : investment : dividends"   : "income, dividend"
        # PITFALL: "infrequent income" includes inheritance.
        # Since this dictionary is used to compute total cash income,
        # the renaming of the innheritance variable is handled separately.
        , 'total income, monthly : infrequent'       : "income, infrequent"
        , 'total income, monthly : govt, cash'       : "income, govt, cash"
        , 'total income, monthly : labor, cash'      : "income, labor, cash"
        , "total income, monthly : private"          : "income, private"
        }
      income_short_name_dict_in_kind = {
          'total income, monthly : govt, in-kind'  : "income, govt, in-kind"
        , 'total income, monthly : labor, in-kind' : "income, labor, in-kind"
        }
      ppl = ppl.rename( columns = { **income_short_name_dict_cash
                                  , **income_short_name_dict_in_kind
      } )
      ppl = ppl.rename( columns =
        { "income, month : infrequent : inheritance"
          : "income, inheritance" } )
      #
    if True: # compute across-category sums
      ppl["income, cash"]    = (
        ppl[ list( income_short_name_dict_cash
                 . values() ) +
             [ "income, rental + interest"
             , "income, sale not real estate"
             , "income, govt edu, cash"
             , "income, month : private : non-beca, cash"
             , "income, month : private : beca, cash"]
        ].sum(axis=1) )
      ppl["income, in-kind"] = (
        ppl[ list( income_short_name_dict_in_kind.values() ) +
             [ "income, govt edu, in-kind"
             , "income, month : private : non-beca, in-kind"
             , "income, month : private : beca, in-kind"]
        ].sum(axis=1) )
      #
      for col in ["income", "income, govt", "income, labor"]:
          ppl[col] = ppl[col + ", cash"] + ppl[col + ", in-kind"]

if True: # compute each household member's income rank
  def sort_household_by_labor_income_then_make_index(df):
    dff = df.sort_values("income, labor", ascending = False)
    dff["member-by-income"] = range(1, len(dff) + 1)
    return dff
  #
  ppl = ppl . groupby('household'
      ) . apply( sort_household_by_labor_income_then_make_index
      ) . drop( columns = "household"
                # one level of the index holds the same information
      ) . reset_index(
      ) . drop( columns = "level_1" )
                # the other part of the index is unneeded

if True: # make|format some categorical variables
  ppl["race, indig"]    = ppl["race"] == 1
  ppl["race, git|rom"]  = ppl["race"] == 2
  ppl["race, raizal"]   = ppl["race"] == 3
  ppl["race, palenq"]   = ppl["race"] == 4
  ppl["race, neg|mul"]  = ppl["race"] == 5
  ppl["race, whi|mest"] = ppl["race"] == 6
  #
  ppl["edu"] = pd.Categorical(
    ppl["edu"
      ] . replace( 9, np.nan
      ) . map( files.edu_key )
    , categories = list( files.edu_key.values() ),
    ordered = True)
  #
  ppl["disabled"] = ppl["why did not seek work"] == 11
  ppl = ppl.drop( columns = "why did not seek work" )
  #
  #time_use_key = { 1 : "work" # Trabajando
  #           , 2 : "search" # Buscando trabajo
  #           , 3 : "study" # Estudiando
  #           , 4 : "household" # Oficios del hogar
  #           , 5 : "disabled" # Incapacitado permanente para trabajar
  #           , 6 : "other" # Otra actividad
  #}
  #ppl["time use"] = pd.Categorical(
  #  ppl["time use"].map( time_use_key ),
  #  categories = list( time_use_key.values() ),
  #  ordered = True)

if True: # dependence
  ppl[ "jefe" ] = ( # head of household
    ppl["relationship"] == 1 )
  #
  ppl[ "relative, child" ] = (
    ( ppl["relationship"] == 3 )     # hijo, hijastro
    | ( ppl["relationship"] == 4 ) ) # nieto
  #
  ppl[ "relative, non-child" ] = (
    ( ppl["relationship"] == 2 )     # Pareja, esposo(a), cónyuge, compañero(a)
    | ( ppl["relationship"] == 5 ) ) # Otro pariente
  #
  ppl["dependent"] = (
      # ASSUMPTION: The labor income < min wage clause is not in the law.
      # However, an accountant has advised us that in practice,
      # children with substantial income are not classified as dependents.
      # The minimum wage threshold is just a guess.
      # Persons making less than it are surely able to hide their income,
      # as they are by definition in the informal sector.
      # Persons making more than it might be able to hide their incomes too;
      # the model will not capture such hiding.
      #
        ( ( ppl["income, labor, cash"] >= c.min_wage )
        & ( ppl["relative, child"]==1 )
        & ( ( ppl["age"] < 19 )
          | ( ( ppl["student"]==1 )
            & ( ppl["age"] < 24 ) )
          | ( ppl["disabled"]==1 ) ) )
      | ( ( ppl["relative, non-child"]==1 )
        & ( ppl["income"] < (260 * c.muvt  ) )
          | ( ppl["disabled"]==1 ) )
      )

if True: # drop vars that are (so far) unused downstream of here
  ppl = ppl.drop( columns =
    [ "income, month : borrowing : from person"
    , "income, month : borrowing : from bank"
    , "income, month : borrowing : from other"
    , "income, month : sale : livestock"
    , "income, month : sale : stock"
    , "income, month : sale : stock ?2"
    , "income, month : sale : vehicle | equipment"
    , "pension, contribution amount"
    , "pre-k|daycare"
    , "race"
    , "relationship"
    , "skipped 3 meals"
    , "income : edu : beca, cash"
    , "income : edu : beca, in-kind"
    , "income : edu : non-beca, cash"
    , "income : edu : non-beca, in-kind"
    , "income, month : govt : beca, cash"
    , "income, month : private : beca, cash"
    , "income, month : govt : non-beca, cash"
    , "income, month : private : non-beca, cash"
    , "income, month : govt : beca, in-kind"
    , "income, month : private : beca, in-kind"
    , "income, month : govt : non-beca, in-kind"
    , "income, month : private : non-beca, in-kind"
    , "jefe"
    , "relative, child"
    , "relative, non-child" ] )
  #
ppl[ "used savings" ] = ppl[ "used savings" ] == 1

oio.saveStage(cl.subsample, ppl, 'people_1')
