wages = pd.Series(
  [ 1e5, min_wage, 2.5e6, 5e6, 8e6, 15e6, 60e6 ] )
asalariados = pd.DataFrame(
  { "wage"       : wages
  , "independiente" : [0,0,0,0,0,0,0] } )
independientes = pd.DataFrame(
  { "wage"       : wages
  , "independiente" : [1,1,1,1,1,1,1] } )

for df in [asalariados, independientes]:
  for (title, compute) in [
        ("tax, pension"               , ss.mk_pension)
      , ("tax, pension, employer"     , ss.mk_pension_employer)
      , ("tax, salud"                 , ss.mk_salud)
      , ("tax, salud, employer"       , ss.mk_salud_employer)
      , ("tax, solidaridad"           , ss.mk_solidaridad)
      , ("tax, parafiscales"          , ss.mk_parafiscales_employer)
      , ("tax, cajas de compensacion" , ss.mk_cajas_de_compensacion_employer)
      , ("cesantias + primas"         , ss.mk_cesantias_employer) ]:
    df[title] = df.apply( lambda row: compute( row["independiente"], row["wage"] )
                          , axis=1
    )

asalariados.to_csv( "output/tests/asalariados_ss_contribs.csv"
                  , index=False
)
independientes.to_csv( "output/tests/independientes_ss_contribs.csv"
                     , index=False
)
