import pandas as pd


df = pd.read_excel( "data/DIAN-quantiles/2-cleaning.xlsx",
                    sheet_name = "Punto 4-AG 2019" )

df.to_csv (
  "data/DIAN-quantiles/individuals.by-patrimonio-liquido.AG-2019.csv",
  index = False )
