import numpy as np
import pandas as pd
import python.vat.build.classes as classes
import python.vat.build.common as common


edu_key = { 1 : "Ninguno",
    2 : "Preescolar",
    3 : "Basica\n Primaria",
    4 : "Basica\n Secundaria",
    5 : "Media",
    6 : "Superior o\n Universitaria",
    9 : "No sabe,\n no informa" }

race_key = { 1 : "Indigena"
    , 2 : "Gitano-Roma"
    , 3 : "Raizal" # "del archipiélago de San Andrés y Providencia"
    , 4 : "Palenquero" # "de San Basilio o descendiente"
    , 5 : "Negro" # "Negro(a), mulato(a), afrocolombiano(a) o afrodescendiente"
    , 6 : "Ninguno" # "Ninguno de los anteriores (mestizo, blanco, etc.)"
    }

demog = {
    "P6050"      : "relationship"
  , "P6020"      : "female"
  , "P6040"      : "age"
  , "P6080"      : "race"
  , "P5170"      : "pre-k|daycare"
  , "P6060"      : "skipped 3 meals"
  , "P6160"      : "literate"
  , "P6170"      : "student"
  , "P6210"      : "education" # highest level completed
  , "P6430"      : "independiente" # 1-3 = asalariado; 4-5 = independiente
                                # other = no income
}

income_govt = {
    "P9460S1"    : "income, month : govt : unemployment"
  , "P1668S1A1"  : "income, year : govt : familias en accion"
  , "P1668S3A2"  : "income, year : govt : familias en su tierra"
  , "P1668S4A2"  : "income, year : govt : jovenes en accion"
  , "P1668S2A2"  : "income, year : govt : programa de adultos mayores"
  , "P1668S5A2"  : "income, year : govt : transferencias por victimizacion"
  , "P1668S1A4"  : "income, year : govt : familias en accion, in-kind"
  , "P1668S3A4"  : "income, year : govt : familias en su tierra, in-kind"
  , "P1668S4A4"  : "income, year : govt : jovenes en accion, in-kind"
  , "P1668S2A4"  : "income, year : govt : programa de adultos mayores, in-kind"
  , "P1668S5A4"  : "income, year : govt : transferencias por victimizacion, in-kind"
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

  , "P7510S9A1"  : "income, year : sale : ?stock"
  , "P7513S3A1"  : "income, year : sale : livestock"
  , "P7513S1A1"  : "income, year : sale : real estate"
  , "P7513S4A1"  : "income, year : sale : stock ?2"
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
}

beca_sources_private = {
    "P6207M1"  : "beca from same school"
  , "P6207M5"  : "beca from another public entity"
  , "P6207M6"  : "beca from empresa publica ~familiar"
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
    , { **common.variables
      , **demog
      , **income
      , **beca_sources_govt
      , **beca_sources_private
      , "P6236" : "non-beca sources" # PITFALL : a space-separated list of ints
    } , common.corrections
      + [classes.Correction.Drop_Column( "file-origin" )
        ]
) ]

# count public sources of funding in the "non-beca sources" variable
def count_public(list_as_str):
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
