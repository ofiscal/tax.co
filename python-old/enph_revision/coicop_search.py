# exec( open("python/enph_revision/coicop_search.py").read() )

import pandas as pd
import numpy as np
import os


subsample = 10
exec( open("python/enph_revision/define_files_and_folders.py").read() )
exec( open("python/enph_revision/all_data/load.py").read() )
exec( open("python/enph_revision/all_data/clean.py").read() )


bridge_codes = list( coicop_vat["coicop"].unique() )

def overview(codes,source_name,colname,acc):
  print( "Unique values: " + str( len(codes) ) )
  print( "Min, max, range: (" + str( min( codes ) )
         + ", " + str( max( codes ) )
         + ", " + str( max( codes ) - min(codes) )
         + ")" )
  print( "Max length as string: " + str(
    max( [len(str(x)) for x in codes] ) ) )
  unrecognized = set(codes) - set(bridge_codes)
  print( "# of elements not in our list of COICOPs: " + str(
    len( unrecognized ) ) )
  acc.append( (source_name, colname, unrecognized) )

if True: # These two file-columns should (per the documentation) include nothing but COICOP codes
  files_with_coicop = [
    (   gastos_diarios_urbano__comidas_preparadas_fuera
     , "gastos_diarios_urbano__comidas_preparadas_fuera"
     ,   ["nh_cgducfh_p1_1" ]),
    (   gastos_personales_urbano__comidas_preparadas_fuera
     , "gastos_personales_urbano__comidas_preparadas_fuera"
     , ["nh_cgpucfh_p1_s1"])
    ]

if True: # Report the few non-numbers in one file's COICOP-like column
  df = gastos_menos_frecuentes__articulos
  colname = "p10270"
  non_numbers = df[colname].str.contains( "[^0-9\.]", regex=True )
  print( "gastos_menos_frecuentes__articulos[\"" + colname + "\"] contains these non-numbers: " )
  print( str( sorted( df[ non_numbers ][colname].unique() ) ) )
  del(df,colname)

files_maybe_with_coicop = files_with_coicop + [
    (   gastos_diarios_personales_urbano
     , "gastos_diarios_personales_urbano"
     ,  ["nc4_cc_p1_1"])
  , (   gastos_diarios_urbanos
     , "gastos_diarios_urbanos"
     ,  ["nh_cgdu_p1"])

  # the previous section, titled "... nonuniformity ...", explains this
  , (   gastos_menos_frecuentes__articulos[ -non_numbers ]
     , "gastos_menos_frecuentes__articulos, minus the \"inv\" values"
     ,  ["p10270"])

  , (   gastos_personales_rural
     , "gastos_personales_rural"
     ,  ["nc2r_ce_p2"])
  , (   gastos_semanales_rurales
     , "gastos_semanales_rurales"
     ,  ["nc2r_ca_p3"])
  , (   gastos_semanales_rural__capitulo_c
     , "gastos_semanales_rural__capitulo_c"
     ,  ["nc2_cc_p1"])
  , (   gastos_semanales_rural__comidas_preparadas_fuera
     , "gastos_semanales_rural__comidas_preparadas_fuera"
     ,  ["nh_cgprcfh_p1s1"] )
  ]

if True: # Analysis
  acc = []
  print( "\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-")
  for (file,filename,colnames) in files_maybe_with_coicop:
    for colname in colnames:
      col = file[colname]
      col2 = col[ -col.isnull() ]
      df = pd.DataFrame( col2 )
      codes = list( pd.to_numeric( col2 )
                    .unique() )
      print( "\n" + filename + "[\"" + colname + "\"]")
      overview( codes, df, colname, acc )

if True: # Result
  unrecognized_from_all_files = sorted( list( pd.Series(
      [x for (_,_,unrecognized) in acc for x in unrecognized]
    ).unique() ) )
  print( "\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-")
  print( "Total number of unrecognized COICOP codes: " + str( len( unrecognized_from_all_files ) ) + "\n")
  target = open( output_folder + "unrecognized_coicop_codes.txt", "w+")
  for x in unrecognized_from_all_files: target.write( str(x) + "\n" )
  target.close()
