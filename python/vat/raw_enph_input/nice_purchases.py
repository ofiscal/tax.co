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
  )

  , File( "urban_diario_fuera"
    , "Gastos_diarios_del_hogar_Urbano_-_Comidas_preparadas_fuera_del_hogar.csv"
    , {"NH_CGDUCFH_P1_1" : "coicop"
       ,"NH_CGDUCFH_P2" : "quantity"
       ,"NH_CGDUCFH_P3" : "how-got"
       ,"NH_CGDUCFH_P4" : "where-got"
       ,"NH_CGDUCFH_P5" : "value"
       ,"NH_CGDUCFH_P6" : "freq"
    }
  )

  , File( "urban_diario_personal"
    , "Gastos_diarios_personales_Urbano.csv"
    , {"NC4_CC_P1_1" : "coicop"
      ,"NC4_CC_P2" : "quantity"
      ,"NC4_CC_P3" : "how-got"
      ,"NC4_CC_P4" : "where-got"
      ,"NC4_CC_P5" : "value"
      ,"NC4_CC_P6" : "freq"
    }
  )

  , File( "urban_diario"
    , "Gastos_diarios_Urbanos.csv"
    , { "P10250S1A1" : "drop-observastion-if-present"
      # almost always missing. if not missing, drop observation -- it records a within-household transfer of money
        ,"NH_CGDU_P1" : "coicop"
        ,"NH_CGDU_P2" : "quantity"
        ,"NH_CGDU_P5" : "how-got"
        ,"NH_CGDU_P7B1379" : "where-got"
        ,"NH_CGDU_P8" : "value"
        ,"NH_CGDU_P9" : "freq"
    }
  )

  , File( "rural_personal_fuera"
    , "Gastos_personales_Rural_-_Comidas_preparadas_fuera_del_Hogar.csv"
    , {"NC2R_CA_P3" : " coicop"
       ,"NC2R_CA_P4_S1" : "quantity"
       ,"NC2R_CA_P5_S1" : "how-got"
       ,"NC2R_CA_P6_S1" : "where-got"
       ,"NC2R_CA_P7_S1" : "value"
       ,"NC2R_CA_P8_S1" : "freq"
    }
  )

  , File( "rural_personal"
    , "Gastos_personales_Rural.csv"
    , {"NC2R_CE_P2" : "coicop"
       ,"NC2R_CE_P4S1" : "quantity"
       ,"NC2R_CE_P5S2" : "how-got"
       ,"NC2R_CE_P6" : "where-got"
       ,"NC2R_CE_P7" : "value"
       ,"NC2R_CE_P8" : "freq"
    }
  )

  , File( "rural_semanal_fuera"
    , "Gastos_semanales_Rural_-_Comidas_preparadas_fuera_del_hogar.csv"
    , {"NH_CGPRCFH_P1S1" : "coicop"
       ,"NH_CGPRCFH_P2" : "quantity"
       ,"NH_CGPRCFH_P3" : "how-got"
       ,"NH_CGPRCFH_P4" : "where-got"
       ,"NH_CGPRCFH_P5" : "value"
       ,"NH_CGPRCFH_P6" : "freq"
    }
  )

  , File( "rural_semanal"
    , "Gastos_semanales_Rurales.csv"
    , {"NC2R_CA_P3" : " coicop"
       ,"NC2R_CA_P4_S1" : "quantity"
       ,"NC2R_CA_P5_S1" : "how-got"
       ,"NC2R_CA_P6_S1" : "where-got"
       ,"NC2R_CA_P7_S1" : "value"
       ,"NC2R_CA_P8_S1" : "freq"
    }
  )
]