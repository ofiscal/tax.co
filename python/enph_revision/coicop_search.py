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

if True: # These two file-columns should (per the documentation) include nothing but known COICOP codes
  files_with_coicop = [
    (   gastos_diarios_urbano__comidas_preparadas_fuera
     , "gastos_diarios_urbano__comidas_preparadas_fuera"
     ,   ["nh_cgducfh_p1_1" ]),
    (   gastos_personales_urbano__comidas_preparadas_fuera
     , "gastos_personales_urbano__comidas_preparadas_fuera"
     , ["nh_cgpucfh_p1_s1"])
    ]

if True: # handle the nonuniformity in one file's COICOP-like column
  df = gastos_menos_frecuentes__articulos
  colname = "p10270"
  invs = df[colname].str.contains( "[^0-9\.]", regex=True )
  print( "gastos_menos_frecuentes__articulos[\"" + colname + "\"] contains these non-numbers: " )
  print( str( sorted( df[ invs ][colname].unique() ) ) )
  del(df,colname)

files_maybe_with_coicop = files_with_coicop + [
    (   gastos_diarios_personales_urbano
     , "gastos_diarios_personales_urbano"
     ,  ["nc4_cc_p1_1"])
  , (   gastos_diarios_urbanos
     , "gastos_diarios_urbanos"
     ,  ["nh_cgdu_p1"])

  # the previous section, titled "... nonuniformity ...", explains this
  , (   gastos_menos_frecuentes__articulos[ -invs ]
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
  for (file,name,colnames) in files_maybe_with_coicop:
    for colname in colnames:
      codes = list( pd.to_numeric( file[colname] )
                    .unique() )
      print( "\n" + name + "[\"" + colname + "\"]")
      overview( codes, file, colname, acc )

if True: # Result
  unrecognized_from_all_files = sorted( list( pd.Series(
      [x for (_,_,unrecognized) in acc for x in unrecognized]
    ).unique() ) )
  print( "Total number of unrecognized COICOP codes: " + str( len( unrecognized_from_all_files ) ) )
  target = open( output_folder + "unrecognized_coicop_codes.txt", "w+")
  for x in unrecognized_from_all_files: target.write( str(x) + "\n" )
  target.close()
