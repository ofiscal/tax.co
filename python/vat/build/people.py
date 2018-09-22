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
      , "P6170"      : "student"
      , "P8610"      : "beca"
      , "P6060"      : "skipped 3 meals"
      , "P6160"      : "literate"
      , "P6210"      : "education" # highest level completed
      , "P6240"      : "time use"
      , "P6300"      : "want to work"
      , "P6800"      : "hours worked, usual"
      , "P6850"      : "hours worked, last week"
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
