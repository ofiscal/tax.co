import pandas as pd
import python.vat.build.classes as classes
import python.vat.build.common as common


files = [
  classes.File( "people"
    , "Caracteristicas_generales_personas.csv"
    , { **common.variables
      , "P6020"      : "female"
      , "P6040"      : "age"
      , "P6080"      : "race"
      , "P5170"      : "pre-k|daycare"
      , "P6060"      : "skipped 3 meals"
      , "P6160"      : "literate"
      , "P6170"      : "student"
      , "P6210"      : "education" # highest level completed

      , "P7500S2A1"  : "income, month : benefit : pension for age | illness"
      , "P9460S1"    : "income, month : benefit : unemployment"

      , "P7510S6A1"  : "income, year : benefit : cesantia"
      , "P1668S1A1"  : "income, year : benefit : familias en accion"
      , "P1668S3A2"  : "income, year : benefit : familias en su tierra"
      , "P1668S4A2"  : "income, year : benefit : jovenes en accion"
      , "P1668S2A2"  : "income, year : benefit : programa de adultos mayores"
      , "P1668S5A2"  : "income, year : benefit : transferencias por victimizacion"
      , "P1668S1A4"  : "income, year : benefit : familias en accion, in-kind"
      , "P1668S3A4"  : "income, year : benefit : familias en su tierra, in-kind"
      , "P1668S4A4"  : "income, year : benefit : jovenes en accion, in-kind"
      , "P1668S2A4"  : "income, year : benefit : programa de adultos mayores, in-kind"
      , "P1668S5A4"  : "income, year : benefit : transferencias por victimizacion, in-kind"

      , "P6500"      : "income, month : labor : formal employment"
      , "P7070"      : "income, month : labor : job 2"
      , "P7472S1"    : "income, month : labor : as inactive"
      , "P7422S1"    : "income, month : labor : as unemployed"
      , "P6750"      : "income, month : labor : independent"
      , "P6760"       : "income, month : labor : independent, months"
                       # divide P6750 by this to get monthly
                       # hopefully this is usually 1 or missing

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

      , "P8610S2"    : "income, year : grant : edu, beca, in-kind"
      , "P8612S2"    : "income, year : grant : edu, non-beca, in-kind"

      , "P8610S1"    : "income, year : grant : edu, beca"
      , "P8612S1"    : "income, year : grant : edu, non-beca"
      , "P7510S3A1"  : "income, year : grant : from private domestic ?firms"
      , "P7510S4A1"  : "income, year : grant : from private foreign ?firms"
      , "P7510S1A1"  : "income, year : grant : remittance, domestic"
      , "P7510S2A1"  : "income, year : grant : remittance, foreign"

      , "P7513S9A1"  : "income, year : infrequent : gambling"
      , "P7513S10A1" : "income, year : infrequent : inheritance"
      , "P7513S8A1"  : "income, year : infrequent : jury awards"
      , "P7513S12A1" : "income, year : infrequent : refund, other"
      , "P7513S11A1" : "income, year : infrequent : refund, tax"

      , "P7510S10A1" : "income, year : investment : dividends"
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

# Earlier names this code used for the income in the official ENPH release
#       , "P7422S1"    : "labor income, ?1"
#       , "P6500"      : "labor income, formal" # the quantity referred to by the "overlooked" questions
#       , "P7472S1"    : "labor income, ?2"
#       , "P6510S1"    : "labor income, overtime"
#       , "P6510S2"    : "labor income, overtime overlooked"
#       , "P6750"      : "labor income, contractor"
#       , "P550"       : "labor income, rural business"
#       , "P7500S1A1"  : "rental income, building"
#       , "P7500S4A1"  : "rental income, land"
#       , "P7500S5A1"  : "rental income, vehicles and equipment"
#       , "P7510S5A1"  : "investment income, interest+"
#       , "P7510S10A1" : "investment income, dividend"
#       , "P7510S9A1"  : "investment income, sale"
#       , "P7500S2A1"  : "benefit income, pension+"
#       , "P7500S3A1"  : "benefit income, alimony"
#       , "P7510S1A1"  : "benefit income, remittance, native"
#       , "P7510S2A1"  : "benefit income, remittance, foreign"
#       , "P7510S3A1"  : "benefit income, charity, native"
#       , "P7510S4A1"  : "benefit income, charity, foreign"
#       , "P7510S6A1"  : "benefit income, layoff"
#       , "P1668S1A1"  : "benefit income, Mas Familias en Accion"
#       , "P1668S2A2"  : "benefit income, Programas de Adultos Mayores"
#       , "P1668S3A2"  : "benefit income, Familias en su Tierra"
#       , "P1668S4A2"  : "benefit income, Jovenes en Accion"
#       , "P1668S5A2"  : "benefit income, Transferencias por Victimizacion"
    } , common.corrections
      + [classes.Correction.Drop_Column( "file-origin" )
        ]
) ]
