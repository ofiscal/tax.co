import sys
import numpy as np
import pandas as pd
import re as regex

import python.build.common as common
import python.build.people.files as files
import python.build.output_io as oio


people = common.to_numbers(
  common.collect_files( files.files
                        , subsample = common.subsample )
  , skip_columns = ["non-beca sources"] # PITFALL : a space-separated list of ints
)

if True: # drop non-members of household
  people = people.drop(
    people[
      people["relationship"].isin( [6,7,8] )
    ].index )

if True: # make independiente a 0 or a 1
  people["independiente"] = people[ "independiente"
                         ] . apply( lambda x: 1 if x in [4,5] else 0 )

if True: # remap some boolean integers
  for cn in ( [ "female" ] +                           # originally 1=male, 2=female
              [included for (quantity,included) in files.inclusion_pairs]
                # originally 1=included, 2=forgot
  ): people[cn] = people[cn] - 1

  for cn in [ "student"         # originally 1=student, 2=not
            , "skipped 3 meals" # originally 1=yes, 2=no
            , "literate"        # originally 1=yes, 2=no
  ]: people[cn] = 2 - people[cn]

if True: # income
  if True: # fill NaN values (one column's with 1, the rest's with 0)
    people[   "income, month : labor : independent, months" ] = (
      people[ "income, month : labor : independent, months" ] . fillna(1) )

    re = regex.compile( ".*income.*" )
    income_columns = [c for c in people.columns if re.match( c )]
    columns_to_convert = ( income_columns
                         + list( files.beca_sources_private.values() )
                         + list( files.beca_sources_govt.values() ) )
    people[columns_to_convert] = people[columns_to_convert] . fillna(0)
    for c in columns_to_convert: # 98 and 99 are error codes -- "doesn't know" and "won't say"
      people[c] = people[c].apply(
        lambda x : 0 if ((x >= 98) & (x <= 99)) else x )
    del(re, income_columns, columns_to_convert)

  if True: # divide yearly income variables by 12
    re_year_income  = regex.compile( "^income, year" )
    for c in [c for c in people.columns if re_year_income.match( c )]:
      people[c] = people[c] / 12

  # PITFALL : Yearly income variables have now been divided by 12, but their names are unchanged.
    # (Once all the totals have been computed, those components will have all been dropped,
    # but until then it could be confusing.)

  re_in_kind       = regex.compile( "^income.* : .* : .* in.kind$" )

  if True: # compute income totals, drop components
    if True: # divide educational income by source (government or private)
      people["non-beca sources"] = people["non-beca sources"] . apply( str )
        # because if none of the values included more than one source (true
        # in subsamples), it was by default interpreted as a number.

      people["non-beca sources, govt"] = people["non-beca sources"
                                         ] . apply( files.count_public )
      people["non-beca sources, private"] = people["non-beca sources"
                                         ] . apply( files.count_private )
      people["non-beca sources, total"] = ( people["non-beca sources, govt"]
                                          + people["non-beca sources, private"] )

      people["beca sources, govt"]    = people[ list( files.beca_sources_govt   .values()
                                        ) ] . sum( axis=1 )
      people["beca sources, private"] = people[ list( files.beca_sources_private.values()
                                        ) ] . sum( axis=1 )
      people["beca sources, total"] = ( people["beca sources, govt"]
                                      + people["beca sources, private"] )

      people["income, month : govt : beca"]        = ( people["income, year : edu : beca"]
        * people["beca sources, govt"]    / people["beca sources, total"] )
      people["income, month : private : beca"]     = ( people["income, year : edu : beca"]
        * people["beca sources, private"] / people["beca sources, total"] )
      people["income, month : govt : non-beca"]    = ( people["income, year : edu : non-beca"]
        * people["non-beca sources, govt"]    / people["non-beca sources, total"] )
      people["income, month : private : non-beca"] = ( people["income, year : edu : non-beca"]
        * people["non-beca sources, private"] / people["non-beca sources, total"] )

      people["income, month : govt : beca, in-kind"]        = (
        people["income, year : edu : beca, in-kind"]
        * people["beca sources, govt"]    / people["beca sources, total"] )
      people["income, month : private : beca, in-kind"]     = (
        people["income, year : edu : beca, in-kind"]
        * people["beca sources, private"]    / people["beca sources, total"] )
      people["income, month : govt : non-beca, in-kind"]    = (
        people["income, year : edu : non-beca, in-kind"]
        * people["non-beca sources, govt"]    / people["non-beca sources, total"] )
      people["income, month : private : non-beca, in-kind"] = (
        people["income, year : edu : non-beca, in-kind"]
        * people["non-beca sources, private"]    / people["non-beca sources, total"] )

      new_income_variables = people.filter(
        regex = "^income, month : (govt|private) : (beca|non-\beca)" )
      new_income_variables.fillna(0)

      del(new_income_variables)
      people = people.drop( columns =
                            people.filter( regex = "(^beca)|(edu : .*beca)|(beca source)"
                            ).columns )

    if True: # govt income (cash + in-kind)
      re_govt  = regex.compile( "^income.* : govt" )
      cols_govt_cash    = [ c for c in people.columns
                               if re_govt.match(c) and not re_in_kind.match(c) ]
      cols_govt_in_kind = [ c for c in people.columns
                               if re_govt.match(c) and     re_in_kind.match(c) ]
      people["total income, monthly : govt, cash"] = (
        people[ cols_govt_cash ].sum( axis=1 ) )
      people["total income, monthly : govt, in-kind"] = (
        people[ cols_govt_in_kind ].sum( axis=1 ) )
      people = people.drop( columns = cols_govt_in_kind + cols_govt_cash )

    if True: # capital income (cash only)
      re_capital = regex.compile( "^income.* : (investment|repayment|rental|sale) : .*" )
      cols_capital = [ c for c in people.columns
                       if re_capital.match(c) ]
      people["total income, monthly : capital"] = (
        people[ cols_capital ].sum( axis=1 ) )

      # drop most components, but keep dividend income, and create capital minus dividends
      people = people.drop( columns = list( set ( cols_capital )
                                          - set ( ["income, year : investment : dividends"] )
      ) )
      people["income, capital w/o dividends"] = people["total income, monthly : capital"
                                                ] - people["income, year : investment : dividends"]

    if True: # private income (cash + in-kind)
      re_private  = regex.compile( "^income.* : private : " )
      cols_private_cash    = [ c for c in people.columns
                               if re_private.match(c) and not re_in_kind.match(c) ]
      cols_private_in_kind = [ c for c in people.columns
                               if re_private.match(c) and     re_in_kind.match(c) ]
      people["total income, monthly : private, cash"] = (
        people[ cols_private_cash ].sum( axis=1 ) )
      people["total income, monthly : private, in-kind"] = (
        people[ cols_private_in_kind ].sum( axis=1 ) )
      people = people.drop( columns = cols_private_in_kind + cols_private_cash )

    if True: # infrequent income (cash only)
      re_infrequent = regex.compile( "^income, year : infrequent : " )
      cols_infrequent = [ c for c in people.columns
                       if re_infrequent.match(c) ]
      people["total income, monthly : infrequent"] = (
        people[ cols_infrequent ].sum( axis=1 ) )
      people = people.drop( columns = cols_infrequent )

    if True: # labor income
      if True: # normalize independent labor income to one months' worth
        s = "income, month : labor : independent"
        people[s] = people[s] * people[s + ", months"]
        people = people.drop( columns = [s + ", months"] )
        del(s)

      if True: # after this, we can simply sum all monthly labor income variables
        for (quantity, forgot) in files.inclusion_pairs:
          people[ quantity ] = people[ quantity ] * people[ forgot ]
        people = people.drop( columns = [ forgot for (_, forgot) in files.inclusion_pairs ] )

      if True: # compute within-category sums
        re_labor  = regex.compile( "^income.* : labor : " )
        cols_labor_cash    = [ c for c in people.columns
                                 if re_labor.match(c) and not re_in_kind.match(c) ]
        cols_labor_in_kind = [ c for c in people.columns
                                 if re_labor.match(c) and     re_in_kind.match(c) ]
        people["total income, monthly : labor, cash"] = (
          people[ cols_labor_cash ].sum( axis=1 ) )
        people["total income, monthly : labor, in-kind"] = (
          people[ cols_labor_in_kind ].sum( axis=1 ) )
        people = people.drop( columns = cols_labor_in_kind + cols_labor_cash )

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
        people = people.rename( columns = { **income_short_name_dict_cash
                                          , **income_short_name_dict_in_kind
        } )

      if True: # compute across-category sums
        people["income, cash"]    = people[ list( income_short_name_dict_cash   .values() )
                                    ].sum(axis=1)
        people["income, in-kind"] = people[ list( income_short_name_dict_in_kind.values() )
                                    ].sum(axis=1)

        for c in ["income", "income, govt", "income, private", "income, labor"]:
            people[c] = people[c + ", cash"] + people[c + ", in-kind"]

if True: # compute each household member's income rank
  def sort_household_by_labor_income_then_make_index(df):
    dff = df.sort_values("income, labor", ascending = False)
    dff["member-by-income"] = range(1, len(dff) + 1)
    return dff

  people = people . groupby('household'
                ) . apply( sort_household_by_labor_income_then_make_index
                ) . drop( columns = "household" # one level of the index holds the same information
                ) . reset_index(
                ) . drop( columns = "level_1" ) # the other part of the index is unneeded

if True: # format some categorical variables
  people["race"] = pd.Categorical(
    people["race"].map( files.race_key )
    , categories = list( files.race_key.values() )
    , ordered = True)
  people["race, indig"]    = people["race"] == 1
  people["race, git|rom"]  = people["race"] == 2
  people["race, raizal"]   = people["race"] == 3
  people["race, palenq"]   = people["race"] == 4
  people["race, neg|mul"]  = people["race"] == 5
  people["race, whi|mest"] = people["race"] == 6

  people["education"] = pd.Categorical(
    people["education"
      ] . fillna( 9
      ) . map( files.edu_key )
    , categories = list( files.edu_key.values() ),
    ordered = True)

  #time_use_key = { 1 : "work" # Trabajando
  #           , 2 : "search" # Buscando trabajo
  #           , 3 : "study" # Estudiando
  #           , 4 : "household" # Oficios del hogar
  #           , 5 : "disabled" # Incapacitado permanente para trabajar
  #           , 6 : "other" # Otra actividad
  #}
  #people["time use"] = pd.Categorical(
  #  people["time use"].map( time_use_key ),
  #  categories = list( time_use_key.values() ),
  #  ordered = True)

oio.saveStage(common.subsample, people, 'people_1')
