import python.enph_revision.define_files_and_folders as filetree


coicop_vat = pd.read_csv( "data/vat/coicop-vat.csv", sep=';' )


if True: # files that identify purchases via a COICOP
  # PITFALL: The default behavior of read_csv is to alphabetize columns.
  # Some of these shenanigans are to make columns appear in the order stated.
  cols = [ "NH_CGDUCFH_P1_1" # COICOP
         , "NH_CGDUCFH_P1"   # verbal
  ]
  gastos_diarios_urbano__comidas_preparadas_fuera    = pd.read_csv(
    filetree.new_folder + "Gastos_diarios_del_hogar_Urbano_-_Comidas_preparadas_fuera_del_hogar.csv",
    index_col=False,
    usecols = cols
  )[cols]
  cols = ["NC4_CC_P1_1"]
  gastos_diarios_personales_urbano                   = pd.read_csv(
    filetree.new_folder + "Gastos_diarios_personales_Urbano.csv",
    index_col=False,
    usecols = cols
  )[cols]
  cols = ["NH_CGDU_P1"]
  gastos_diarios_urbanos                             = pd.read_csv(
    filetree.new_folder + "Gastos_diarios_Urbanos.csv", 
    index_col=False,   
    usecols = cols
  )[cols]
  cols = ["P10270"]
  gastos_menos_frecuentes__articulos                 = pd.read_csv(
    filetree.new_folder + "Gastos_menos_frecuentes_-_Articulos.csv",
    index_col=False,
    usecols = cols
  )[cols]
  cols = ["NC2R_CA_P3"]
  gastos_personales_rural__comidas_preparadas_fuera  = pd.read_csv(
    filetree.new_folder + "Gastos_personales_Rural_-_Comidas_preparadas_fuera_del_Hogar.csv",
    index_col=False,
    usecols = cols
  )[cols]
  cols = ["NC2R_CE_P2"]
  gastos_personales_rural                            = pd.read_csv(
    filetree.new_folder + "Gastos_personales_Rural.csv",
    index_col=False,
    usecols = cols
  )[cols]
  cols = [ "NH_CGPUCFH_P1"    # COICOP
            , "NH_CGPUCFH_P1_S1" # verbal
  ]
  gastos_personales_urbano__comidas_preparadas_fuera = pd.read_csv(
    filetree.new_folder + "Gastos_personales_Urbano_-_Comidas_preparadas_fuera_del_hogar.csv",
    usecols = cols
  )[cols]
  cols = [ "NH_CGPRCFH_P1"   # COICOP
         , "NH_CGPRCFH_P1S1" # verbal
  ] 
  gastos_semanales_rural__comidas_preparadas_fuera   = pd.read_csv(
    filetree.new_folder + "Gastos_semanales_Rural_-_Comidas_preparadas_fuera_del_hogar.csv",
    usecols = cols
  )[cols]
  cols = ["NC2R_CA_P3"]
  gastos_semanales_rurales                           = pd.read_csv(
    filetree.new_folder + "Gastos_semanales_Rurales.csv",
    usecols = cols
  )[cols]
  del(cols)


if True: # files that identify purchases without a COICOP
  gastos_menos_frecuentes__medio_de_pago             = pd.read_csv(
    filetree.new_folder + "Gastos_menos_frecuentes_-_Medio_de_pago.csv",
    usecols = [ "P10305" # says whether a house is new or old
              , "P10305S1" # value of the purchase
  ] )
  gastos_semanales_rural__capitulo_c                 = pd.read_csv(
    filetree.new_folder + "Gastos_semanales_Rural_-_Capitulo_C.csv",
    usecols = ["NC2_CC_P1" # 25 broad categories.
  ] )


newEnphsDfs = [
              # caracteristicas_generales_personas
                gastos_diarios_urbano__comidas_preparadas_fuera
              , gastos_diarios_personales_urbano
              , gastos_diarios_urbanos
              # , gastos_diarios_urbanos__mercados
              , gastos_menos_frecuentes__articulos
              , gastos_menos_frecuentes__medio_de_pago
              , gastos_personales_rural__comidas_preparadas_fuera
              , gastos_personales_rural
              , gastos_personales_urbano__comidas_preparadas_fuera
              , gastos_semanales_rural__capitulo_c
              , gastos_semanales_rural__comidas_preparadas_fuera
              , gastos_semanales_rurales
              # , gastos_semanales_rurales__mercados
              # , viviendas_y_hogares
              ]

