import sys
import numpy as np
import pandas as pd
import re as regex

import python.common.misc as c
import python.common.cl_args as cl
import python.build.people.files as files
import python.build.output_io as oio


ppl = c.to_numbers(
  cl.collect_files( files.files
                  , subsample = cl.subsample )
  , skip_columns = ["non-beca sources"] # PITFALL : a space-separated list of ints
)

ppl = ppl.drop( # drop non-members of household
  ppl[ ppl["relationship"].isin( [6,7,8] )
  ].index )

if True: # make independiente a 0 or a 1
  ppl["independiente"] = ppl[ "independiente"
                         ] . apply( lambda x: 1 if x in [4,5] else 0 )

if True: # remap some boolean integers
  for cn in ( [ "female" ] + # originally 1=male, 2=female
              [included for (quantity,included) in files.inclusion_pairs]
                             # originally 1=included, 2=forgot
  ): ppl[cn] = ppl[cn] - 1

  for cn in [ "student"         # originally 1=student, 2=not
            , "skipped 3 meals" # originally 1=yes, 2=no
            , "literate"        # originally 1=yes, 2=no
  ]: ppl[cn] = 2 - ppl[cn]

if True: # non-income work characteristics
  ppl["pension, contributing (if not pensioned)"] = (
    ppl["pension, contributing, pre"]
    . apply( lambda x: 1 if x==1 else ( 0 if x==2 else np.nan ) ) )

  ppl["pension, receiving"] = (
      ( ppl["pension, contributing, pre"] == 3 )
    | ( ppl["income, month : pension : age | illness"] > 0 )
  ) . astype('int')

  ppl["pension, contributor(s) (if not pensioned) = split"] = (
    ppl["pension, contributors, pre"]
    . apply( lambda x: 1 if x == 1 else
             ( 0 if (x > 0) & (x < 4) else np.nan ) ) )

  ppl["pension, contributor(s) (if not pensioned) = self"] = (
    ppl["pension, contributors, pre"]
    . apply( lambda x: 1 if x == 2 else
             ( 0 if (x > 0) & (x < 4) else np.nan ) ) )

  ppl["pension, contributor(s) (if not pensioned) = employer"] = (
    ppl["pension, contributors, pre"]
    . apply( lambda x: 1 if x == 3 else
             ( 0 if (x > 0) & (x < 4) else np.nan ) ) )

  ppl["seguro de riesgos laborales (if reported)"] = (
    ppl["seguro de riesgos laborales, pre"]
    . apply( lambda x: 1 if x==1 else
             ( 0 if x==2 else np.nan ) ) )

  ppl.drop( columns = [ "pension, contributing, pre"
                      , "pension, contributors, pre"
                      , "seguro de riesgos laborales, pre" ] )

if True: # income
  if True: # fill NaN values (one column's with 1, the rest's with 0)
    ppl[   "income, month : labor : independent, months" ] = (
      ppl[ "income, month : labor : independent, months" ] . fillna(1) )

    re = regex.compile( ".*income.*" )
    income_columns = [col for col in ppl.columns if re.match( col )]
    columns_to_convert = ( income_columns
                         + list( files.beca_sources_private.values() )
                         + list( files.beca_sources_govt.values() ) )
    ppl[columns_to_convert] = ppl[columns_to_convert] . fillna(0)
    for col in columns_to_convert: # 98 and 99 are error codes for
                                   # "doesn't know" and "won't say"
      ppl[col] = ppl[col].apply(
        lambda x : 0 if ((x >= 98) & (x <= 99)) else x )
    del(re, income_columns, columns_to_convert)

  if True: # divide yearly income variables by 12
    re_year_income  = regex.compile( "^income, year" )
    for col in [col for col in ppl.columns if re_year_income.match( col )]:
      ppl[col] = ppl[col] / 12

  # PITFALL : Yearly income variables have now been divided by 12,
  # but their names are unchanged.
    # (Once all the totals have been computed, those components will have
    #  all been dropped, but until then it could be confusing.)

  re_in_kind = regex.compile( "^income.* : .* : .* in.kind$" )

  if True: # compute income totals, drop components
    if True: # divide educational income by source (government or private)
      ppl["non-beca sources"] = ppl["non-beca sources"] . apply( str )
        # because if none of the values included more than one source (true
        # in subsamples), it was by default interpreted as a number.

      ppl["non-beca sources, govt"] = ppl["non-beca sources"
                                      ] . apply( files.count_public )
      ppl["non-beca sources, private"] = ppl["non-beca sources"
                                         ] . apply( files.count_private )
      ppl["non-beca sources, total"] = ( ppl["non-beca sources, govt"]
                                       + ppl["non-beca sources, private"] )

      ppl["beca sources, govt"]    = ppl[ list( files.beca_sources_govt   .values()
                                     ) ] . sum( axis=1 )
      ppl["beca sources, private"] = ppl[ list( files.beca_sources_private.values()
                                     ) ] . sum( axis=1 )
      ppl["beca sources, total"] = ( ppl["beca sources, govt"]
                                   + ppl["beca sources, private"] )

      ppl["income, month : govt : beca"]        = (
        ppl["income, year : edu : beca"]
        * ppl["beca sources, govt"]    / ppl["beca sources, total"] )
      ppl["income, month : private : beca"]     = (
        ppl["income, year : edu : beca"]
        * ppl["beca sources, private"] / ppl["beca sources, total"] )
      ppl["income, month : govt : non-beca"]    = (
        ppl["income, year : edu : non-beca"]
        * ppl["non-beca sources, govt"]    / ppl["non-beca sources, total"] )
      ppl["income, month : private : non-beca"] = (
        ppl["income, year : edu : non-beca"]
        * ppl["non-beca sources, private"] / ppl["non-beca sources, total"] )

      ppl["income, month : govt : beca, in-kind"]        = (
        ppl["income, year : edu : beca, in-kind"]
        * ppl["beca sources, govt"]    / ppl["beca sources, total"] )
      ppl["income, month : private : beca, in-kind"]     = (
        ppl["income, year : edu : beca, in-kind"]
        * ppl["beca sources, private"]    / ppl["beca sources, total"] )
      ppl["income, month : govt : non-beca, in-kind"]    = (
        ppl["income, year : edu : non-beca, in-kind"]
        * ppl["non-beca sources, govt"]    / ppl["non-beca sources, total"] )
      ppl["income, month : private : non-beca, in-kind"] = (
        ppl["income, year : edu : non-beca, in-kind"]
        * ppl["non-beca sources, private"]    / ppl["non-beca sources, total"] )

      new_income_variables = ppl.filter(
        regex = "^income, month : (govt|private) : (beca|non-\beca)" )
      new_income_variables.fillna(0)

      del(new_income_variables)
      ppl = ppl.drop(
        columns = ppl.filter( regex = "(^beca)|(edu : .*beca)|(beca source)"
        ).columns )

    if True: # govt income (cash + in-kind)
      re_govt  = regex.compile( "^income.* : govt" )
      cols_govt_cash    = [ col for col in ppl.columns
                          if re_govt.match(col) and not re_in_kind.match(col) ]
      cols_govt_in_kind = [ col for col in ppl.columns
                          if re_govt.match(col) and     re_in_kind.match(col) ]
      ppl["total income, monthly : govt, cash"] = (
        ppl[ cols_govt_cash ].sum( axis=1 ) )
      ppl["total income, monthly : govt, in-kind"] = (
        ppl[ cols_govt_in_kind ].sum( axis=1 ) )
      ppl = ppl.drop( columns = cols_govt_in_kind + cols_govt_cash )

    if True: # capital income (cash only)
      re_capital = regex.compile(
        "^income.* : (investment|rental|sale) : .*" )
      cols_capital = [ col for col in ppl.columns
                     if re_capital.match(col) ]
      ppl["total income, monthly : capital"] = (
        ppl[ cols_capital ].sum( axis=1 ) )

      # drop most components, but keep dividend income,
      # and create capital minus dividends
      ppl = ppl.drop(
        columns = list( set ( cols_capital )
                      - set ( ["income, year : investment : dividends"] )
      ) )
      ppl["income, capital w/o dividends"] = (
        ppl["total income, monthly : capital"
        ] - ppl["income, year : investment : dividends"] )

    if True: # private income (cash + in-kind)
      re_private  = regex.compile( "^income.* : private : " )
      cols_private_cash    = [ col for col in ppl.columns
                             if re_private.match(col) and not re_in_kind.match(col) ]
      cols_private_in_kind = [ col for col in ppl.columns
                             if re_private.match(col) and     re_in_kind.match(col) ]
      ppl["total income, monthly : private, cash"] = (
        ppl[ cols_private_cash ].sum( axis=1 ) )
      ppl["total income, monthly : private, in-kind"] = (
        ppl[ cols_private_in_kind ].sum( axis=1 ) )
      ppl["income, donacion"] = (
        # PITFALL: overlaps what will be called "income, private"
        ppl["income, year : private : from private domestic ?firms"] +
        ppl["income, year : private : from private foreign ?firms"] )

      ppl = ppl.drop( columns = cols_private_in_kind + cols_private_cash )

    if True: # infrequent income (cash only)
      re_infrequent = regex.compile( "^income, year : infrequent : " )
      cols_infrequent = [ col for col in ppl.columns
                        if re_infrequent.match(col) ]
      ppl["total income, monthly : infrequent"] = (
        ppl[ cols_infrequent ].sum( axis=1 ) )
      ppl["income, ganancia ocasional"] = (
        # PITFALL: overlaps what will be called "income, infrequent"
        ppl["income, year : infrequent : gambling"] +
        ppl["income, year : infrequent : inheritance"] )
      ppl["income, indemnizacion"] = (
        # PITFALL: overlaps what will be called "income, infrequent"
        ppl["income, year : infrequent : jury awards"] )

      ppl = ppl.drop( columns = cols_infrequent )

    if True: # "income" from borrowing
      re_borrowing = regex.compile( "^income.* : borrowing : .*" )
      cols_borrowing = [ col for col in ppl.columns
                      if re_borrowing.match(col) ]
      ppl["total income, monthly : borrowing"] = (
        ppl[ cols_borrowing ].sum( axis=1 ) )

    if True: # labor income
      if True: # normalize independent labor income to one months' worth
        s = "income, month : labor : independent"
        ppl[s] = ppl[s] * ppl[s + ", months"]
        ppl = ppl.drop( columns = [s + ", months"] )
        del(s)

      if True: # after this, we can simply sum all monthly labor income variables
        for (quantity, forgot) in files.inclusion_pairs:
          ppl[ quantity ] = ppl[ quantity ] * ppl[ forgot ]
        ppl = ppl.drop(
          columns = [ forgot for (_, forgot) in files.inclusion_pairs ] )

      if True: # compute within-category sums
        re_labor  = regex.compile( "^income.* : labor : " )
        cols_labor_cash    = [ col for col in ppl.columns
                             if re_labor.match(col) and not re_in_kind.match(col) ]
        cols_labor_in_kind = [ col for col in ppl.columns
                             if re_labor.match(col) and     re_in_kind.match(col) ]
        ppl["total income, monthly : labor, cash"] = (
          ppl[ cols_labor_cash ].sum( axis=1 ) )
        ppl["total income, monthly : labor, in-kind"] = (
          ppl[ cols_labor_in_kind ].sum( axis=1 ) )
        ppl = ppl.drop( columns = cols_labor_in_kind + cols_labor_cash )

      if True: # homogenize, shorten income variable names
        income_short_name_dict_cash = {
            'income, month : pension : age | illness'  : "income, pension"
          , 'income, year : cesantia'                  : "income, cesantia"
          , 'total income, monthly : capital'          : "income, capital"
          , "income, year : investment : dividends"    : "income, capital, dividends"
          , 'total income, monthly : infrequent'       : "income, infrequent"
          , 'total income, monthly : govt, cash'       : "income, govt, cash"
          , 'total income, monthly : private, cash'    : "income, private, cash"
          , 'total income, monthly : labor, cash'      : "income, labor, cash"
          }
        income_short_name_dict_in_kind = {
            'total income, monthly : govt, in-kind'    : "income, govt, in-kind"
          , 'total income, monthly : private, in-kind' : "income, private, in-kind"
          , 'total income, monthly : labor, in-kind'   : "income, labor, in-kind"
          }
        ppl = ppl.rename( columns = { **income_short_name_dict_cash
                                          , **income_short_name_dict_in_kind
        } )

      if True: # compute across-category sums
        ppl["income, cash"]    = (
          ppl[ list( income_short_name_dict_cash   .values() )
          ].sum(axis=1) )
        ppl["income, in-kind"] = (
          ppl[ list( income_short_name_dict_in_kind.values() )
          ].sum(axis=1) )

        for col in ["income", "income, govt", "income, private", "income, labor"]:
            ppl[col] = ppl[col + ", cash"] + ppl[col + ", in-kind"]

if True: # compute each household member's income rank
  def sort_household_by_labor_income_then_make_index(df):
    dff = df.sort_values("income, labor", ascending = False)
    dff["member-by-income"] = range(1, len(dff) + 1)
    return dff

  ppl = ppl . groupby('household'
      ) . apply( sort_household_by_labor_income_then_make_index
      ) . drop( columns = "household"
                # one level of the index holds the same information
      ) . reset_index(
      ) . drop( columns = "level_1" )
                # the other part of the index is unneeded

if True: # format some categorical variables
  ppl["race"] = pd.Categorical(
    ppl["race"].map( files.race_key )
    , categories = list( files.race_key.values() )
    , ordered = True)
  ppl["race, indig"]    = ppl["race"] == 1
  ppl["race, git|rom"]  = ppl["race"] == 2
  ppl["race, raizal"]   = ppl["race"] == 3
  ppl["race, palenq"]   = ppl["race"] == 4
  ppl["race, neg|mul"]  = ppl["race"] == 5
  ppl["race, whi|mest"] = ppl["race"] == 6

  ppl["education"] = pd.Categorical(
    ppl["education"
      ] . fillna( 9
      ) . map( files.edu_key )
    , categories = list( files.edu_key.values() ),
    ordered = True)

  ppl["disabled"] = ppl["why did not seek work"] == 11
  ppl = ppl.drop( columns = "why did not seek work" )

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

  ppl[ "relative, child" ] = (
    ( ppl["relationship"] == 3 )     # hijo, hijastro
    | ( ppl["relationship"] == 4 ) ) # nieto

  ppl[ "relative, non-child" ] = (
    ( ppl["relationship"] == 2 )     # Pareja, esposo(a), cónyuge, compañero(a)
    | ( ppl["relationship"] == 5 ) ) # Otro pariente

  ppl["dependent"] = ( ( ( ppl["relative, child"]==1 )
                       & ( ( ppl["age"] < 19 )
                         | ( ( ppl["student"]==1 )
                           & ( ppl["age"] < 24 ) )
                         | ( ppl["disabled"]==1 ) ) )
                     | ( ( ppl["relative, non-child"]==1 )
                       & ( ppl["income"] < (260 * c.uvt / 12  ) )
                         | ( ppl["disabled"]==1 ) )
                     )

oio.saveStage(cl.subsample, ppl, 'people_1')
