import pandas as pd
from python.build.classes import File, Correction, StringProperty
import python.common.misc as c


files = [

  File( "rural_personal"
    , "Gastos_personales_Rural.csv"
    , c.variables_with_comma_weight +
      [ ( "NC2R_CE_P2",   { StringProperty.NotAString }, "coicop", 0 )
      , ( "NC2R_CE_P4S1", { StringProperty.HasNull
                          , StringProperty.Comma
                          , StringProperty.Digits}, "quantity", 0 )
      , ( "NC2R_CE_P5S2", { StringProperty.NotAString }, "how-got", 0 )
      , ( "NC2R_CE_P6",   { StringProperty.NotAString }, "where-got", 0 )
      , ( "NC2R_CE_P7",   { StringProperty.NotAString }, "value", 0 )
      , ( "NC2R_CE_P8",   { StringProperty.NotAString }, "freq", 0 ) ]
    , c.corrections
  )

  , File( "rural_personal_fuera"
    , "Gastos_personales_Rural_-_Comidas_preparadas_fuera_del_Hogar.csv"
    , c.variables_with_comma_weight +
      [ ( "NC2R_CA_P3",    { StringProperty.NotAString }, "coicop", 0 )
      , ( "NC2R_CA_P4_S1", { StringProperty.Digits
                           , StringProperty.Comma
                           , StringProperty.HasNull }, "quantity", 0 )
      , ( "NC2R_CA_P5_S1", { StringProperty.NotAString }, "how-got", 0 )
      , ( "NC2R_CA_P6_S1", { StringProperty.NotAString }, "where-got", 0 )
      , ( "NC2R_CA_P7_S1", { StringProperty.NotAString }, "value", 0 )
      , ( "NC2R_CA_P8_S1", { StringProperty.NotAString }, "freq", 0 ) ]
    , c.corrections
  )

  , File( "rural_semanal"
    , "Gastos_semanales_Rurales.csv"
    , c.variables_with_comma_weight +
      [ ( "NC2R_CA_P3",    { StringProperty.NotAString }, "coicop", 0 )
      , ( "NC2R_CA_P4_S1", { StringProperty.HasNull
                           , StringProperty.Comma
                           , StringProperty.Digits}, "quantity", 0 )
      , ( "NC2R_CA_P5_S1", { StringProperty.NotAString }, "how-got", 0 )
      , ( "NC2R_CA_P6_S1", { StringProperty.NotAString }, "where-got", 0 )
      , ( "NC2R_CA_P7_S1", { StringProperty.NotAString }, "value", 0 )
      , ( "NC2R_CA_P8_S1", { StringProperty.NotAString }, "freq", 0 ) ]
    , c.corrections
  )

  , File( "rural_semanal_fuera"
    , "Gastos_semanales_Rural_-_Comidas_preparadas_fuera_del_hogar.csv"
    , c.variables_with_comma_weight +
      [ ( "NH_CGPRCFH_P1S1", { StringProperty.NotAString }, "coicop", 0 )
      , ( "NH_CGPRCFH_P2"  , { StringProperty.HasNull
                             , StringProperty.Comma
                             , StringProperty.Digits }, "quantity", 0 )
      , ( "NH_CGPRCFH_P3"  , { StringProperty.NotAString }, "how-got", 0 )
      , ( "NH_CGPRCFH_P4"  , { StringProperty.NotAString }, "where-got", 0 )
      , ( "NH_CGPRCFH_P5"  , { StringProperty.NotAString }, "value", 0 )
      , ( "NH_CGPRCFH_P6"  , { StringProperty.NotAString }, "freq", 0 ) ]
    , c.corrections
  )

  , File( "urban_diario"
    , "Gastos_diarios_Urbanos.csv"
    , c.variables +
      [ ( "P10250S1A1",      { StringProperty.NotAString }, "within-household-transfer", 0 )
      , ( "NH_CGDU_P1",      { StringProperty.NotAString }, "coicop", 0 )
      , ( "NH_CGDU_P2",      { StringProperty.NotAString }, "quantity", 0 )
      , ( "NH_CGDU_P5",      { StringProperty.NotAString }, "how-got", 0 )
      , ( "NH_CGDU_P7B1379", { StringProperty.NotAString }, "where-got", 0 )
      , ( "NH_CGDU_P8",      { StringProperty.NotAString }, "value", 0 )
      , ( "NH_CGDU_P9",      { StringProperty.NotAString }, "freq", 0 ) ]
    , c.corrections
      + [ # The "within-household transfer" variable is almost always null. If it's not,
        # drop the observation. Then drop that column.
        Correction.Drop_Row_If_Column_Satisfies_Predicate( "within-household-transfer"
                                                         , pd.notnull
                                                         )
        , Correction.Drop_Column( "within-household-transfer" )
      ]
  )

  , File( "urban_diario_fuera"
    , "Gastos_diarios_del_hogar_Urbano_-_Comidas_preparadas_fuera_del_hogar.csv"
    , c.variables_with_comma_weight +
      [ ( "NH_CGDUCFH_P1_1", { StringProperty.NotAString }, "coicop", 0 )
      , ( "NH_CGDUCFH_P2",   { StringProperty.Comma
                             , StringProperty.Digits } , "quantity", 0 )
      , ( "NH_CGDUCFH_P3",   { StringProperty.NotAString }, "how-got", 0 )
      , ( "NH_CGDUCFH_P4",   { StringProperty.NotAString }, "where-got", 0 )
      , ( "NH_CGDUCFH_P5",   { StringProperty.NotAString }, "value", 0 )
      , ( "NH_CGDUCFH_P6",   { StringProperty.NotAString }, "freq", 0 ) ]
    , c.corrections
  )

  , File( "urban_diario_personal"
    , "Gastos_diarios_personales_Urbano.csv"
    , c.variables_with_comma_weight +
      [ ( "NC4_CC_P1_1", { StringProperty.NotAString }, "coicop", 0 )
      , ( "NC4_CC_P2",   { StringProperty.Comma
                         , StringProperty.Digits }, "quantity", 0 )
      , ( "NC4_CC_P3",   { StringProperty.NotAString }, "how-got", 0 )
      , ( "NC4_CC_P4",   { StringProperty.NotAString }, "where-got", 0 )
      , ( "NC4_CC_P5",   { StringProperty.NotAString }, "value", 0 )
      , ( "NC4_CC_P6",   { StringProperty.NotAString }, "freq", 0 ) ]
    , c.corrections
  )

  , File( "urban_personal_fuera"
    , "Gastos_personales_Urbano_-_Comidas_preparadas_fuera_del_hogar.csv"
    , c.variables_with_comma_weight +
      [ ( "NH_CGPUCFH_P1_S1", { StringProperty.NotAString }, "coicop", 0 )
      , ( "NH_CGPUCFH_P2",    { StringProperty.Comma
                              , StringProperty.Digits }, "quantity", 0 )
      , ( "NH_CGPUCFH_P3",    { StringProperty.NotAString }, "how-got", 0 )
      , ( "NH_CGPUCFH_P4",    { StringProperty.NotAString }, "where-got", 0 )
      , ( "NH_CGPUCFH_P5",    { StringProperty.NotAString }, "value", 0 )
      , ( "NH_CGPUCFH_P6",    { StringProperty.NotAString }, "freq", 0 ) ]
    , c.corrections
  )
]
