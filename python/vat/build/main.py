import pandas as pd
import numpy as np
import re as regex

from python.vat.build.classes import Correction
import python.vat.build.common as common

# input files
import python.vat.build.purchases.nice_purchases as nice_purchases
import python.vat.build.purchases.medios as medios
import python.vat.build.purchases.articulos as articulos
import python.vat.build.purchases.capitulo_c as capitulo_c
import python.vat.build.people.files as ppl


if True: # purchases
  purchases = common.collect_files(
    articulos.files
    # + medios.files
      # The tax only applies if the purchase is more than 880 million pesos,
      # and the data only records purchases of a second home.
    + capitulo_c.files
    + nice_purchases.files
  )

  for c in [ # TODO ? This might be easier to understand without the Correction class.
    Correction.Replace_Substring_In_Column( "quantity", ",", "." )
    , Correction.Replace_Missing_Values( "quantity", 1 )

    , Correction.Change_Column_Type( "coicop", str )
    , Correction.Replace_Entirely_If_Substring_Is_In_Column( "coicop", "inv", np.nan )

    # The rest of these variables need the same number-string-cleaning process:
      , Correction.Change_Column_Type( "where-got", str )
        # same as this: purchases["where-got"] = purchases["where-got"] . astype( str )
      , Correction.Replace_In_Column( "where-got"
                                    , { ' ' : np.nan
                                      , "nan" : np.nan } ) # 'nan's are created from the cast to type str
        # same as this: purchases["where-got"] = purchases["where-got"] . replace( <that same dictionary> )

      , Correction.Change_Column_Type( "freq", str )
      , Correction.Replace_In_Column( "freq"
                                    , { ' ' : np.nan
                                      , "nan" : np.nan } )

      , Correction.Change_Column_Type( "how-got", str )
      , Correction.Replace_In_Column( "how-got"
                                    , { ' ' : np.nan
                                      , "nan" : np.nan } )

      , Correction.Change_Column_Type( "value", str )
      , Correction.Replace_In_Column( "value"
                                    , { ' ' : np.nan
                                      , "nan" : np.nan } )
  ]: purchases = c.correct( purchases )

  purchases = common.to_numbers(purchases)

  purchases = purchases[ # must have a value and a coicop-like variable
    ( (  ~ purchases[ "coicop"          ] . isnull())
      | (~ purchases[ "25-broad-categs" ] . isnull()) )
    & (  ~ purchases[ "value"           ] . isnull())
  ]
    # Why: For every file but "articulos", observations with no coicop have
    # no value, quantity, is-purchase or frequency. And only 63 / 211,000
    # observations in "articulos" have a missing COICOP. A way see that:
      # df0 = data.purchases[ data.purchases[ "coicop" ] . isnull() ]
      # util.dwmByGroup( "file-origin", df0 )

  for c in [
    Correction.Apply_Function_To_Column(
      "how-got"
      , lambda x: 1 if x==1 else
        # HACK: x >= 0 yields true for numbers, false for NaN
        (0 if x >= 0 else np.nan) )
    , Correction.Rename_Column( "how-got", "is-purchase" )
  ]: purchases = c.correct( purchases )


if False: # people
  people = common.to_numbers( common.collect_files( ppl.files ) )

  if True: # remap some boolean integers
    for cn in ( [ "female" ] +                           # originally 1=male, 2=female
                [included for (quantity,included) in ppl.inclusion_pairs]
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
      people[ income_columns ] = people[income_columns] . fillna(0)
      del(re, income_columns)

    if True: # divide yearly income variables by 12
      re_year_income  = regex.compile( "^income, year" )
      for c in [c for c in people.columns if re_year_income.match( c )]:
        people[c] = people[c] / 12

    # PITFALL : Yearly income variables have now been divided by 12, but their names are unchanged.
      # (Once all the totals have been computed, those components will have all been dropped,
      # but until then it could be confusing.)

    re_in_kind       = regex.compile( "^income.* : .* : .* in.kind$" )

    if True: # compute income totals, drop components
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
          for (quantity, forgot) in ppl.inclusion_pairs:
            people[ quantity ] = people[ quantity ] * people[ forgot ]
          people = people.drop( columns = [ forgot for (_, forgot) in ppl.inclusion_pairs ] )
    
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
