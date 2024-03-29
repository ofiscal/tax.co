person_file_legend = { "directorio" : "household"
                     , "orden"      : "household-member"
                     , "p6160"      : "literate"
                     , "p6170"      : "student"
                     , "p6430"      : "employer type"
                     , "p6500"      : "income"
                     , "p6040"      : "age"
                     , "p6080"      : "race"
                     , "p6020"      : "female"
                     , "p6210"      : "education"
                     , "p6370"      : "job name (text)"
                     , "p6370s1"    : "job code" }

frequency_legend = {
  1 : 1,   # » 2. Diario
  2 : 3.5, # » 2.1 Varias veces por semana
           # 3.5 is the arithmetic average of the numbers in [1,7].
           # The geometric average is 3.38.
  3 : 7,   # » 3.Semanal
  4 : 15,  # » 4. Quincenal
  5 : 30,  # » 5. Mensual
  6 : 60,  # » 6. Bimestral
  7 : 90,  # » 7. Trimestral
  8 : 365, # » 8. Anual
  9 : (3*365), # » 9.Esporádico
  10 : 182.5,  # » 10. Semestral
}
frequency_legend = { k : ((365/12)/v) for k,v in frequency_legend.items() }
  # Frontload the division, rather than performing it for each row of data.
  # (Because multiplication is cheaper than division.)

purchase_file_legends = { # keys are filenames
            # values are dictionaries from column names to their meaning
  "st2_sea_enc_gcfhr_ce_csv" : { "nc2r_ce_p2"   : "coicop"
                               , "directorio"   : "household"
                               , "orden"        : "household-member"
                               , "nc2r_ce_p4s1" : "quantity"
                               , "nc2r_ce_p4s2" : "unit-of-measure"
                               , "nc2r_ce_p5"   : "purchased=1"
                               , "nc2r_ce_p6"   : "where-bought"
                               , "nc2r_ce_p7"   : "value"
                               , "nc2r_ce_p8"   : "frequency" }
  , "st2_sea_enc_gcfhr_csv" : { "nh_cgprcfh_p1"   : "good-in-words"
                              , "nh_cgprcfh_p1s1" : "coicop"
                              , "directorio"   : "household"
                              , "orden"        : "household-member"
                              , "nh_cgprcfh_p2"   : "quantity"
                              , "nh_cgprcfh_p3"   : "purchased=1"
                              , "nh_cgprcfh_p4"   : "where-bought"
                              , "nh_cgprcfh_p5"   : "value"
                              , "nh_cgprcfh_p6"   : "frequency"
                              , "nh_cgprcfh_p7"   : "household-communal" }
  , "st2_sea_enc_gcfhu_diarios_csv" : {
      "nh_cgducfh_p1"   : "good-in-words"
    , "nh_cgducfh_p1_1" : "coicop"
    , "directorio"   : "household"
    , "orden"        : "household-member"
    , "nh_cgducfh_p2"   : "quantity"
    , "nh_cgducfh_p3"   : "purchased=1"
    , "nh_cgducfh_p4"   : "where-bought"
    , "nh_cgducfh_p5"   : "value"
    , "nh_cgducfh_p6"   : "frequency"
    , "nh_cgducfh_p7"   : "household-communal" }
  , "st2_sea_enc_gcfhup_diarios_csv" : {
      "nh_cgpucfh_p1"    : "good-in-words"
    , "nh_cgpucfh_p1_s1" : "coicop"
    , "directorio"   : "household"
    , "orden"        : "household-member"
    , "nh_cgpucfh_p2"    : "quantity"
    , "nh_cgpucfh_p3"    : "purchased=1"
    , "nh_cgpucfh_p4"    : "where-bought"
    , "nh_cgpucfh_p5"    : "value"
    , "nh_cgpucfh_p6"    : "frequency" }
  , "st2_sea_enc_gdr_csv" : {
      "nc2r_ca_p3" : "coicop"
    , "directorio"   : "household"
    , "orden"        : "household-member"
    , "nc2r_ca_p4_s1" : "quantity"
    , "nc2r_ca_p4_s2" : "unit-of-measure"
    , "nc2r_ca_p5_s1" : "purchased=1"
    , "nc2r_ca_p6_s1" : "where-bought"
    , "nc2r_ca_p7_s1" : "value"
    , "nc2r_ca_p8_s1" : "frequency" }
  , "st2_sea_enc_gmf_csv" : {
      "p10270" : "coicop"
    , "directorio"   : "household"
    , "orden"        : "household-member"
    , "p10270_fc_s1" : "purchased=1"
    , "p10270s1" : "value(total/cash)"
    , "p10270s2" : "where-bought"
    , "p10270s3" : "frequency"
    , "p10270s4" : "value(credit)"
    }
  , "st2_sea_enc_gsdp_diarios_csv" : {
     "nc4_cc_p1_1" : "coicop"
    , "directorio"   : "household"
    , "orden"        : "household-member"
    , "nc4_cc_p2" : "quantity"
    , "nc4_cc_p3" : "purchased=1"
    , "nc4_cc_p4" : "where-bought"
    , "nc4_cc_p5" : "value"
    , "nc4_cc_p6" : "frequency" }
  , "st2_sea_enc_gsdu_diarios_csv" : {
      "nh_cgdu_p1" : "coicop"
    , "directorio"   : "household"
    , "orden"        : "household-member"
    , "nh_cgdu_p2" : "quantity"
    , "nh_cgdu_p3" : "unit-of-measure"
    , "nh_cgdu_p5" : "purchased=1"
    , "nh_cgdu_p7b1379" : "where-bought"
    , "nh_cgdu_p8" : "value"
    , "nh_cgdu_p9" : "frequency"
    , "nh_cgdu_p10" : "household-communal"
    }
}

# # This appears never to get used, so I have commented it out.
# format_purchase_fields_as_strings = {}
# for filename in purchase_file_legends.keys():
#   x = {}
#   for v2 in purchase_file_legends[filename].values():
#     x[v2] = 'str'
#   format_purchase_fields_as_strings[filename] = x
