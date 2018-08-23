bridge_codes = list( coicop_vat["coicop"].unique() )

def overview(codes,source_name,colname,acc):
  print( "Unique values: " + str( len(codes) ) )
  print( "Max: " + str( max( codes ) ) )
  print( "Max length as string: " + str(
    max( [len(str(x)) for x in codes] ) ) )
  unrecognized = set(codes) - set(bridge_codes)
  print( "# of elements not in our list of COICOPs: " + str(
    len( unrecognized ) ) )
  acc.append( (source_name, colname, unrecognized) )

if True: # Two file-columns should include nothing but known COICOP codes
  files_with_coicop = [
    (gastos_diarios_urbano__comidas_preparadas_fuera,   ["nh_cgducfh_p1_1" ]),
    (gastos_personales_urbano__comidas_preparadas_fuera, ["nh_cgpucfh_p1_s1"])
    ]
  comida_codes = []
  for (file,colnames) in files_with_coicop:
    for colname in colnames:
      comida_codes += list( file[colname].unique() )
  comida_codes = list( set( comida_codes ) )

if True: # Verifying that what should be known codes are at least mostly known
  acc = []
  print( "Verifying that comida_codes are known: " )
  overview( list( comida_codes ), "two of the comida_fuera files"
            , "nh_cgducfh_p1_1  &  nh_cgpucfh_p1_s1", acc )
  acc

files_maybe_with_coicop = [
    (   gastos_diarios_personales_urbano
     , "gastos_diarios_personales_urbano"
     ,  ["nc4_cc_p1_1"])
  , (   gastos_diarios_urbanos
     , "gastos_diarios_urbanos"
     ,  ["nh_cgdu_p1"])
  , (   gastos_menos_frecuentes__articulos
     , "gastos_menos_frecuentes__articulos"
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

acc = []
for (file,name,colnames) in files_maybe_with_coicop:
  for colname in colnames:
    codes = list( file[colname].unique() )
    print( "\n" + name + "[\"" + colname + "\"]")
    overview( codes, file, colname, acc )
