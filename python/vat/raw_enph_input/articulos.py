import pandas as pd
import python.vat.raw_enph_input.config as raw_enph
from python.vat.raw_enph_input.classes import File

files = [
  File( "urban_personal_fuera"
    , "Gastos_personales_Urbano_-_Comidas_preparadas_fuera_del_hogar.csv"
    , { "NH_CGPUCFH_P1_S1" : "coicop"
        ,"NH_CGPUCFH_P2" : "quantity"
        ,"NH_CGPUCFH_P3" : "how-got"
        ,"NH_CGPUCFH_P4" : "where-got"
        ,"NH_CGPUCFH_P5" : "value"
        ,"NH_CGPUCFH_P6" : "freq"
    }
  ) ]
