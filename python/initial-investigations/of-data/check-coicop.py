import pandas as pd
import python.datafiles as datafiles

# (filename,colname) = ("st2_sea_enc_gcfhr_ce_csv","nc2r_ce_p2")
# df = pd.read_csv( datafiles.folder(2017) + "recip-100/" + filename + ".csv")
# col=df[colname]
# print( filename + "." + colname + ": " + str(col.count()) + " / " + str(len(col.index))
#        + " = " + str(col.count() / len(col.index)) + " non-null items" )

fileColumnPairs = [ ("st2_sea_enc_gcfhr_ce_csv", "nc2r_ce_p2")
                    , ("st2_sea_enc_gcfhr_csv", "nh_cgprcfh_p1s1")
                    , ("st2_sea_enc_gcfhu_diarios_csv", "nh_cgducfh_p1_1")
                    , ("st2_sea_enc_gcfhup_diarios_csv", "nh_cgpucfh_p1_s1")
                    , ("st2_sea_enc_gdr_csv", "nc2r_ca_p3")
                    , ("st2_sea_enc_gmf_csv", "p10270")
                    , ("st2_sea_enc_gsdp_diarios_csv", "nc4_cc_p1_1")
                    , ("st2_sea_enc_gsdu_diarios_csv", "nh_cgdu_p1")
]

for (filename,colname) in fileColumnPairs:
  df = pd.read_csv( datafiles.folder(2017) + "recip-100/" + filename + ".csv")
  col=df[colname]
  print( filename + "." + colname + ":\n\t"
         + str(col.count()) + " / " + str(len(col.index))
         + " = "
         + str(col.count() / len(col.index))
         + " non-null items" )
