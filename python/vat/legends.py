nice_files = {
  "personales_urbano_fuera" : {"nh_cgpucfh_p1_s1" : "coicop"
                              ,"nh_cgpucfh_p2" : "quantity"
                              ,"nh_cgpucfh_p3" : "how-got"
                              ,"nh_cgpucfh_p4" : "where-got"
                              ,"nh_cgpucfh_p5" : "value"
                              ,"nh_cgpucfh_p6" : "freq"
                              }

  , "diarios_urbano_fuera" : {"nh_cgducfh_p1_1" : "coicop"
                             ,"nh_cgducfh_p2" : "quantity"
                             ,"nh_cgducfh_p3" : "how-got"
                             ,"nh_cgducfh_p4" : "where-got"
                             ,"nh_cgducfh_p5" : "value"
                             ,"nh_cgducfh_p6" : "freq"
                             }

  , "diarios_personales_urbano" : {"nc4_cc_p1_1" : "coicop"
                                  ,"nc4_cc_p2" : "quantity"
                                  ,"nc4_cc_p3" : "how-got"
                                  ,"nc4_cc_p4" : "where-got"
                                  ,"nc4_cc_p5" : "value"
                                  ,"nc4_cc_p6" : "freq"
                                  }

  , "diarios_urbanos" : {
    "p10250s1a1" : "drop-observastion-if-present"
      # almost always missing. if not missing, drop observation -- it records a within-household transfer of money
    ,"nh_cgdu_p1" : "coicop"
    ,"nh_cgdu_p2" : "quantity"
    ,"nh_cgdu_p5" : "how-got"
    ,"nh_cgdu_p7b1379" : "where-got"
    ,"nh_cgdu_p8" : "value"
    ,"nh_cgdu_p9" : "freq"
    }

  , "personales_rural_fuera" : {"nc2r_ca_p3" : " coicop"
                               ,"nc2r_ca_p4_s1" : "quantity"
                               ,"nc2r_ca_p5_s1" : "how-got"
                               ,"nc2r_ca_p6_s1" : "where-got"
                               ,"nc2r_ca_p7_s1" : "value"
                               ,"nc2r_ca_p8_s1" : "freq"
                               }

  , "personales_rurales" : {"nc2r_ce_p2" : "coicop"
                           ,"nc2r_ce_p4s1" : "quantity"
                           ,"nc2r_ce_p5s2" : "how-got"
                           ,"nc2r_ce_p6" : "where-got"
                           ,"nc2r_ce_p7" : "value"
                           ,"nc2r_ce_p8" : "freq"
                           }

  , "semanales_rural_fuera" : {"nh_cgprcfh_p1s1" : "coicop"
                              ,"nh_cgprcfh_p2" : "quantity"
                              ,"nh_cgprcfh_p3" : "how gotten"
                              ,"nh_cgprcfh_p4" : "where gotten"
                              ,"nh_cgprcfh_p5" : "value"
                              ,"nh_cgprcfh_p6" : "freq"
                              }

  , "semanales_rurales" : {"nc2r_ca_p3" : " coicop"
                          ,"nc2r_ca_p4_s1" : "quantity"
                          ,"nc2r_ca_p5_s1" : "how-got"
                          ,"nc2r_ca_p6_s1" : "where-got"
                          ,"nc2r_ca_p7_s1" : "value"
                          ,"nc2r_ca_p8_s1" : "freq"
                          }
}
