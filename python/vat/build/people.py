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

****** P8610S1 : income, yearly : edu, beca, cash
****** P8610S2 : income, yearly : edu, beca, in-kind
****** P8612S1 : income, yearly : edu, non-beca, cash
****** P8612S2 : income, yearly : edu, non-beca, in-kind

******* P6500 = income, monthly : formal employment
        # was  "P6500"      : "labor income, formal" # the quantity referred to by the "overlooked" questions
******* P6510S1 = income, monthly : overtime
******* P6510S2 = income, monthly : overtime, included in 6500
******* P6590S1 = income, monthly : food, in-kind
******* P6600S1 = income, monthly : lodging, in-kind
******* P6610S1 = income, monthly : transport, in-kind
******* P6620S1 = income, monthly : other, in-kind
******* P6585S1A1 = income subsidy, monthly : food
******* P6585S1A2 = income subsidy, monthly : food, included in 6500
******* P6585S2A1 = income subsidy, monthly : transport
******* P6585S2A2 = income subsidy, monthly : transport, included in 6500
******* P6585S3A1 = income subsidy, monthly : familiar
******* P6585S3A2 = income subsidy, monthly : familiar, included in 6500
******* P1653S1A1 = income, monthly : special bonus
******* P1653S1A2 = income, monthly : special bonus, included in 6500
******* P1653S2A1 = income, monthly : bonus
******* P1653S2A2 = income, monthly : bonus, included in 6500
******* P1653S3A1 = income, monthly : viaticum
******* P1653S3A2 = income, monthly : viaticum, included in 6500
******* P1653S4A1 = income, monthly : gastos de representacion
******* P1653S4A2 = income, monthly : gastos de representacion, included in 6500

******* P6630S1A1 = income, yearly : prima de servicios
******* P6630S2A1 = income, yearly : christmas bonus
******* P6630S3A1 = income, yearly : vacation bonus
******* P6630S4A1 = income, yearly : viaticum
******* P6630S5A1 = income, yearly : bonus
******* P6630S6A1 = income, yearly : work accident payments

      , "P7422S1"    : "labor income, ?1"
      , "P6500"      : "labor income, formal" # the quantity referred to by the "overlooked" questions
      , "P7472S1"    : "labor income, ?2"
      , "P6510S1"    : "labor income, overtime"
      , "P6510S2"    : "labor income, overtime overlooked"
      , "P6750"      : "labor income, contractor"
      , "P550"       : "labor income, rural business"
      , "P7500S1A1"  : "rental income, building"
      , "P7500S4A1"  : "rental income, land"
      , "P7500S5A1"  : "rental income, vehicles and equipment"
      , "P7510S5A1"  : "investment income, interest+"
      , "P7510S10A1" : "investment income, dividend"
      , "P7510S9A1"  : "investment income, sale"
      , "P7500S2A1"  : "benefit income, pension+"
      , "P7500S3A1"  : "benefit income, alimony"
      , "P7510S1A1"  : "benefit income, remittance, native"
      , "P7510S2A1"  : "benefit income, remittance, foreign"
      , "P7510S3A1"  : "benefit income, charity, native"
      , "P7510S4A1"  : "benefit income, charity, foreign"
      , "P7510S6A1"  : "benefit income, layoff"
      , "P1668S1A1"  : "benefit income, Mas Familias en Accion"
      , "P1668S2A2"  : "benefit income, Programas de Adultos Mayores"
      , "P1668S3A2"  : "benefit income, Familias en su Tierra"
      , "P1668S4A2"  : "benefit income, Jovenes en Accion"
      , "P1668S5A2"  : "benefit income, Transferencias por Victimizacion"
    } , common.corrections
      + [classes.Correction.Drop_Column( "file-origin" )
        ]
) ]
