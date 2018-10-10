import pandas as pd
import re as regex

from python.vat.build.classes import Correction
import python.vat.build.common as common

import python.vat.build.people.files as files


people = common.to_numbers( common.collect_files( files.files )
                            , skip_columns = ["non-beca sources"] )

if True: # drop non-members of household
  people = people.drop(
    people[
      people["relationship"].isin( [6,7,8] )
    ].index )

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
        # if none of the values includes more than one source (true in subsamples),
        # it is by default interpreted as a number.

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
    
    if True: # benefit income (cash + in-kind)
      re_benefit  = regex.compile( "^income.* : benefit" )
      cols_benefit_cash    = [ c for c in people.columns
                               if re_benefit.match(c) and not re_in_kind.match(c) ]
      cols_benefit_in_kind = [ c for c in people.columns
                               if re_benefit.match(c) and     re_in_kind.match(c) ]
      people["total income, monthly : benefit, cash"] = (
        people[ cols_benefit_cash ].sum( axis=1 ) )
      people["total income, monthly : benefit, in-kind"] = (
        people[ cols_benefit_in_kind ].sum( axis=1 ) )
      people = people.drop( columns = cols_benefit_in_kind + cols_benefit_cash )

    if True: # capital income (cash only)
      re_capital = regex.compile( "^income.* : (investment|repayment|rental|sale) : .*" )
      cols_capital = [ c for c in people.columns
                       if re_capital.match(c) ]
      people["total income, monthly : capital"] = (
        people[ cols_capital ].sum( axis=1 ) )
      people = people.drop( columns = cols_capital )

    if True: # grant income (cash + in-kind)
      re_grant  = regex.compile( "^income.* : grant : " )
      cols_grant_cash    = [ c for c in people.columns
                               if re_grant.match(c) and not re_in_kind.match(c) ]
      cols_grant_in_kind = [ c for c in people.columns
                               if re_grant.match(c) and     re_in_kind.match(c) ]
      people["total income, monthly : grant, cash"] = (
        people[ cols_grant_cash ].sum( axis=1 ) )
      people["total income, monthly : grant, in-kind"] = (
        people[ cols_grant_in_kind ].sum( axis=1 ) )
      people = people.drop( columns = cols_grant_in_kind + cols_grant_cash )

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

      if True: # compute sums
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

if True: # format some categorical variables
  race_key = {
      1 : "Indigena"
    , 2 : "Gitano-Roma"
    , 3 : "Raizal" # "del archipiélago de San Andrés y Providencia"
    , 4 : "Palenquero" # "de San Basilio o descendiente"
    , 5 : "Negro" # "Negro(a), mulato(a), afrocolombiano(a) o afrodescendiente"
    , 6 : "Ninguno" # "Ninguno de los anteriores (mestizo, blanco, etc.)"
    }
  people["race"] = pd.Categorical(
    people["race"].map( race_key )
    , categories = list( race_key.values() )
    , ordered = True)

  edu_key = { 1 : "Ninguno",
      2 : "Preescolar",
      3 : "Basica\n Primaria",
      4 : "Basica\n Secundaria",
      5 : "Media",
      6 : "Superior o\n Universitaria",
      9 : "No sabe,\n no informa" }
  people["education"] = pd.Categorical(
    people["education"].map( edu_key ),
    categories = list( edu_key.values() ),
    ordered = True)

  #time_key = { 1 : "work" # Trabajando
  #           , 2 : "search" # Buscando trabajo
  #           , 3 : "study" # Estudiando
  #           , 4 : "household" # Oficios del hogar
  #           , 5 : "disabled" # Incapacitado permanente para trabajar
  #           , 6 : "other" # Otra actividad
  #}
  #people["time use"] = pd.Categorical(
  #  people["time use"].map( time_key ),
  #  categories = list( time_key.values() ),
  #  ordered = True)
