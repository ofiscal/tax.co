import numpy                        as np
import pandas                       as pd
import python.build.classes         as classes
import python.build.names_in_tables as n
import python.common.misc           as c
import python.common.cl_args        as cl


edu_key = {
    1 : n.edu_vals.nada
  , 2 : n.edu_vals.pre
  , 3 : n.edu_vals.pri
  , 4 : n.edu_vals.sec
  , 5 : n.edu_vals.med
  , 6 : n.edu_vals.sup
  , 9 : n.edu_vals.no_sabe
}

race_key = {
    1 : n.race_vals.ind
  , 2 : n.race_vals.git
  , 3 : n.race_vals.raiz
  , 4 : n.race_vals.pal
  , 5 : n.race_vals.neg
  , 6 : n.race_vals.nada
}

demog = {
    "P6050" : n.relationship
  , "P6020" : n.female
  , "P6040" : n.age
  , "P6080" : n.race
  , "P5170" : n.pre_k_or_daycare
  , "P6060" : n.skipped_3_meals
  , "P6160" : n.literate
  , "P6170" : n.student
  , "P6210" : n.edu
  , "P6310" : n.why_not_seek_work
  , "P6430" : n.independiente
}

work = { "P6920"   : n.pension_contributing_pre
       , "P6920S1" : n.pension_contribution_amount
       , "P6940"   : n.pension_contributors_pre
       , "P6990"   : n.seguro_laborales
}

income_govt = {
    "P9460S1"   : n.income_month_govt_unemployment
  , "P1668S1A1" : n.income_year_govt_familias_en_accion
  , "P1668S3A2" : n.income_year_govt_familias_en_su_tierra
  , "P1668S4A2" : n.income_year_govt_jovenes_en_accion
  , "P1668S2A2" : n.income_year_govt_programa_de_adultos_mayores
  , "P1668S5A2" : n.income_year_govt_transferencias_por_victimizacion
  , "P1668S1A4" : n.income_year_govt_familias_en_accion_in_kind
  , "P1668S3A4" : n.income_year_govt_familias_en_su_tierra_in_kind
  , "P1668S4A4" : n.income_year_govt_jovenes_en_accion_in_kind
  , "P1668S2A4" : n.income_year_govt_programa_de_adultos_mayores_in_kind
  , "P1668S5A4" : n.income_year_govt_transferencias_por_victimizacion_in_kind
}

income_labor = {
    "P6500"      : "income, month : labor : formal employment"
  , "P7070"      : "income, month : labor : job 2"
  , "P7472S1"    : "income, month : labor : as inactive"
  , "P7422S1"    : "income, month : labor : as unemployed"
  , "P6750"      : "income, month : labor : independent"
  , "P6760"      : "income, month : labor : independent, months"
                   # divide P6750 by this to get monthly
                   # hopefully this is usually 1 or missing

  # below, in the variable `inclusion_pairs`, these are grouped
  , "P1653S1A1"  : "income, month : labor : bonus ?2"
  , "P1653S1A2"  : "income, month : labor : bonus ?2, included in 6500"
  , "P1653S2A1"  : "income, month : labor : bonus"
  , "P1653S2A2"  : "income, month : labor : bonus, included in 6500"
  , "P6585S3A1"  : "income, month : labor : familiar"
  , "P6585S3A2"  : "income, month : labor : familiar, included in 6500"
  , "P6585S1A1"  : "income, month : labor : food"
  , "P6585S1A2"  : "income, month : labor : food, included in 6500"
  , "P1653S4A1"  : "income, month : labor : gastos de representacion"
  , "P1653S4A2"  : "income, month : labor : gastos de representacion, included in 6500"
  , "P6510S1"    : "income, month : labor : overtime"
  , "P6510S2"    : "income, month : labor : overtime, included in 6500"
  , "P6585S2A1"  : "income, month : labor : transport"
  , "P6585S2A2"  : "income, month : labor : transport, included in 6500"
  , "P1653S3A1"  : "income, month : labor : viaticum"
  , "P1653S3A2"  : "income, month : labor : viaticum, included in 6500"

  , "P6779S1"    : "income, month : labor : viaticum ?2"

  , "P550"       : "income, year : labor : rural"
  , "P6630S5A1"  : "income, year : labor : bonus"
  , "P6630S2A1"  : "income, year : labor : christmas bonus"
  , "P6630S1A1"  : "income, year : labor : prima de servicios"
  , "P6630S3A1"  : "income, year : labor : vacation bonus"
  , "P6630S4A1"  : "income, year : labor : viaticum ?3"
  , "P6630S6A1"  : "income, year : labor : work accident payments"

  , "P6590S1"    : "income, month : labor : food, in-kind"
  , "P6600S1"    : "income, month : labor : lodging, in-kind"
  , "P6620S1"    : "income, month : labor : other, in-kind"
  , "P6610S1"    : "income, month : labor : transport, in-kind"
}

income_edu = {
    "P8610S2"    : "income, year : edu : beca, in-kind"
  , "P8612S2"    : "income, year : edu : non-beca, in-kind"
  , "P8610S1"    : "income, year : edu : beca"
  , "P8612S1"    : "income, year : edu : non-beca"
}

income_private = {
    "P7500S3A1"  : "income, month : private : alimony"
  , "P7510S3A1"  : "income, year : private : from private domestic ?firms"
  , "P7510S4A1"  : "income, year : private : from private foreign ?firms"
  , "P7510S1A1"  : "income, year : private : remittance, domestic"
  , "P7510S2A1"  : "income, year : private : remittance, foreign"
}

income_infrequent = {
    "P7513S9A1"  : "income, year : infrequent : gambling"
  , "P7513S10A1" : "income, year : infrequent : inheritance"
  , "P7513S8A1"  : "income, year : infrequent : jury awards"
  , "P7513S12A1" : "income, year : infrequent : refund, other"
  , "P7513S11A1" : "income, year : infrequent : refund, tax"
}

income_capital = {
    "P7510S10A1" : "income, year : investment : dividends"
  , "P7510S5A1"  : "income, year : investment : interest"

  , "P7513S6A1"  : "income, year : repayment : by bank"
  , "P7513S7A1"  : "income, year : repayment : by other"
  , "P7513S5A1"  : "income, year : repayment : by person"

  , "P7500S1A1"  : "income, month : rental : real estate, developed"
  , "P7500S4A1"  : "income, month : rental : real estate, undeveloped"
  , "P7500S5A1"  : "income, month : rental : vehicle | equipment"

  # These two variables record the same information. At least one is always zero.
  # (See python/test/stock_var_non_overlap.py for a proof.)
  # A person's income from sale of stock = their maximum = their sum.
  , "P7510S9A1"  : "income, year : sale : stock"
  , "P7513S4A1"  : "income, year : sale : stock ?2"

  , "P7513S3A1"  : "income, year : sale : livestock"
  , "P7513S1A1"  : "income, year : sale : real estate"
  , "P7513S2A1"  : "income, year : sale : vehicle | equipment"
}

income = { **income_govt
         , **income_labor
         , **income_edu
         , **income_private
         , **income_infrequent
         , **income_capital
         , "P7500S2A1"  : "income, month : pension : age | illness"
         , "P7510S6A1"  : "income, year : cesantia"
}

beca_sources_govt = {
    "P6207M2"  : "beca from ICETEX"
  , "P6207M3"  : "beca from govt, central"
  , "P6207M4"  : "beca from govt, peripheral"
  , "P6207M5"  : "beca from another public entity"
  , "P6207M6"  : "beca from empresa publica ~familiar"
}

beca_sources_private = {
    "P6207M1"  : "beca from same school"
  , "P6207M7"  : "beca from empresa privada ~familiar"
  , "P6207M8"  : "beca from other private"
  , "P6207M9"  : "beca from organismo internacional"
  , "P6207M10" : "beca from Universidades y ONGs"
}

inclusion_pairs = [
     ( "income, month : labor : bonus ?2"
     , "income, month : labor : bonus ?2, included in 6500"
  ), ( "income, month : labor : bonus"
     , "income, month : labor : bonus, included in 6500"
  ), ( "income, month : labor : familiar"
     , "income, month : labor : familiar, included in 6500"
  ), ( "income, month : labor : food"
     , "income, month : labor : food, included in 6500"
  ), ( "income, month : labor : gastos de representacion"
     , "income, month : labor : gastos de representacion, included in 6500"
  ), ( "income, month : labor : overtime"
     , "income, month : labor : overtime, included in 6500"
  ), ( "income, month : labor : transport"
     , "income, month : labor : transport, included in 6500"
  ), ( "income, month : labor : viaticum"
     , "income, month : labor : viaticum, included in 6500"
  ) ]

files = [
  classes.File( "people"
    , "Caracteristicas_generales_personas.csv"
    , { **c.variables
      , **demog
      , **work
      , **income
      , **beca_sources_govt
      , **beca_sources_private
      , "P6236" : "non-beca sources" # PITFALL : a space-separated list of ints
    } , c.corrections
      + [classes.Correction.Drop_Column( "file-origin" )
        ]
) ]

def count_public(list_as_str):
  """Count public sources of funding in the "non-beca sources" variable."""
  stripped = list_as_str . strip()
  if stripped in [np.nan, ""]: return 0
  else:
    num_list = map( float
                  , stripped . split(" ") )
    sources = filter( lambda x: x in [2,3,4], num_list )
    return len( list( sources ) )

# count private sources of funding in the "non-beca sources" variable
def count_private(list_as_str):
  stripped = list_as_str . strip()
  if stripped in [np.nan, ""]: return 0
  else:
    num_list = map( float
                  , stripped . split(" ") )
    sources = filter( lambda x: not x in [2,3,4], num_list )
    return len( list( sources ) )
