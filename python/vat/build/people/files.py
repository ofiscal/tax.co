import pandas as pd
import python.vat.build.classes as classes
import python.vat.build.common as common


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
}

income_benefit = {
    "P7500S2A1"  : "income, month : pension : age | illness"
  , "P9460S1"    : "income, month : govt : unemployment"

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
  , "P7510S6A1"  : "income, year : labor : cesantia"
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

income_grant = {
    "P8610S2"    : "income, year : grant : edu, beca, in-kind"
  , "P8612S2"    : "income, year : grant : edu, non-beca, in-kind"

  , "P8610S1"    : "income, year : grant : edu, beca"
  , "P8612S1"    : "income, year : grant : edu, non-beca"
  , "P7510S3A1"  : "income, year : grant : from private domestic ?firms"
  , "P7510S4A1"  : "income, year : grant : from private foreign ?firms"
  , "P7510S1A1"  : "income, year : grant : remittance, domestic"
  , "P7510S2A1"  : "income, year : grant : remittance, foreign"
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
      , **income_benefit
      , **income_labor
      , **income_grant
      , **income_infrequent
      , **income_capital
    } , common.corrections
      + [classes.Correction.Drop_Column( "file-origin" )
        ]
) ]
