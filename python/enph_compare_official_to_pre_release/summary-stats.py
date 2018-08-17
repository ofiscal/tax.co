import pandas as pd

import python.util as util
import python.enph_compare_official_to_pre_release.files as filetree


exec( open("python/enph_compare_official_to_pre_release/load_files.py").read() )
 
def go                                                (a,b,c,d):
  return util.compare_2_columns_from_different_tables (a,b,c,d)

go( gcfhr, "nh_cgprcfh_p1"  , gastos_semanales_rural__comidas_preparadas_fuera, "nh_cgprcfh_p1" )
go( gcfhr, "nh_cgprcfh_p1s1", gastos_semanales_rural__comidas_preparadas_fuera, "nh_cgprcfh_p1s1" )
go( gcfhr, "nh_cgprcfh_p2"  , gastos_semanales_rural__comidas_preparadas_fuera, "nh_cgprcfh_p2" )
go( gcfhr, "nh_cgprcfh_p3"  , gastos_semanales_rural__comidas_preparadas_fuera, "nh_cgprcfh_p3" )
go( gcfhr, "nh_cgprcfh_p4"  , gastos_semanales_rural__comidas_preparadas_fuera, "nh_cgprcfh_p4" )
go( gcfhr, "nh_cgprcfh_p5"  , gastos_semanales_rural__comidas_preparadas_fuera, "nh_cgprcfh_p5" )
go( gcfhr, "nh_cgprcfh_p6"  , gastos_semanales_rural__comidas_preparadas_fuera, "nh_cgprcfh_p6" )
go( gcfhr, "nh_cgprcfh_p7"  , gastos_semanales_rural__comidas_preparadas_fuera, "nh_cgprcfh_p7" )

go( gcfhu_diarios, "nh_cgducfh_p1"  , gastos_diarios_urbano__comidas_preparadas_fuera, "nh_cgducfh_p1")
go( gcfhu_diarios, "nh_cgducfh_p1_1", gastos_diarios_urbano__comidas_preparadas_fuera, "nh_cgducfh_p1_1")
go( gcfhu_diarios, "nh_cgducfh_p2"  , gastos_diarios_urbano__comidas_preparadas_fuera, "nh_cgducfh_p2")
go( gcfhu_diarios, "nh_cgducfh_p3"  , gastos_diarios_urbano__comidas_preparadas_fuera, "nh_cgducfh_p3")
go( gcfhu_diarios, "nh_cgducfh_p4"  , gastos_diarios_urbano__comidas_preparadas_fuera, "nh_cgducfh_p4")
go( gcfhu_diarios, "nh_cgducfh_p5"  , gastos_diarios_urbano__comidas_preparadas_fuera, "nh_cgducfh_p5")
go( gcfhu_diarios, "nh_cgducfh_p6"  , gastos_diarios_urbano__comidas_preparadas_fuera, "nh_cgducfh_p6")
go( gcfhu_diarios, "nh_cgducfh_p7"  , gastos_diarios_urbano__comidas_preparadas_fuera, "nh_cgducfh_p7")

go( gcfhup_diarios, "nh_cgpucfh_p1"   , gastos_personales_urbano__comidas_preparadas_fuera, "nh_cgpucfh_p1")
go( gcfhup_diarios, "nh_cgpucfh_p1_s1", gastos_personales_urbano__comidas_preparadas_fuera, "nh_cgpucfh_p1_s1")
go( gcfhup_diarios, "nh_cgpucfh_p2"   , gastos_personales_urbano__comidas_preparadas_fuera, "nh_cgpucfh_p2")
go( gcfhup_diarios, "nh_cgpucfh_p3"   , gastos_personales_urbano__comidas_preparadas_fuera, "nh_cgpucfh_p3")
go( gcfhup_diarios, "nh_cgpucfh_p4"   , gastos_personales_urbano__comidas_preparadas_fuera, "nh_cgpucfh_p4")
go( gcfhup_diarios, "nh_cgpucfh_p5"   , gastos_personales_urbano__comidas_preparadas_fuera, "nh_cgpucfh_p5")
go( gcfhup_diarios, "nh_cgpucfh_p6"   , gastos_personales_urbano__comidas_preparadas_fuera, "nh_cgpucfh_p6")

go( gsdp_diarios, "nc4_cc_p1_1", gastos_diarios_personales_urbano, "nc4_cc_p1_1")
go( gsdp_diarios, "nc4_cc_p2"  , gastos_diarios_personales_urbano, "nc4_cc_p2")
go( gsdp_diarios, "nc4_cc_p3"  , gastos_diarios_personales_urbano, "nc4_cc_p3")
go( gsdp_diarios, "nc4_cc_p4"  , gastos_diarios_personales_urbano, "nc4_cc_p4")
go( gsdp_diarios, "nc4_cc_p5"  , gastos_diarios_personales_urbano, "nc4_cc_p5")
go( gsdp_diarios, "nc4_cc_p6"  , gastos_diarios_personales_urbano, "nc4_cc_p6")

go( gsdu_diarios, "nh_cgdu_p1"     , gastos_diarios_urbanos, "nh_cgdu_p1")
go( gsdu_diarios, "nh_cgdu_p2"     , gastos_diarios_urbanos, "nh_cgdu_p2")
go( gsdu_diarios, "nh_cgdu_p3"     , gastos_diarios_urbanos, "nh_cgdu_p3")
go( gsdu_diarios, "nh_cgdu_p5"     , gastos_diarios_urbanos, "nh_cgdu_p5")
go( gsdu_diarios, "nh_cgdu_p7b1379", gastos_diarios_urbanos, "nh_cgdu_p7b1379")
go( gsdu_diarios, "nh_cgdu_p8"     , gastos_diarios_urbanos, "nh_cgdu_p8")
go( gsdu_diarios, "nh_cgdu_p9"     , gastos_diarios_urbanos, "nh_cgdu_p9")
go( gsdu_diarios, "nh_cgdu_p10"    , gastos_diarios_urbanos, "nh_cgdu_p10")
