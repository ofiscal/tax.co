#made by Daniel Duque
import pandas as pd
import os
#Utilidades https://www.dian.gov.co/dian/cifras/Paginas/TributosDIAN.aspx
#https://www.dian.gov.co/dian/cifras/EstadsticasTDIAN/Renta_Naturales_No_Obligadas_2017_F-210.zip
#utilidades es tomado de agregados activ-econom.2017 la suma de rlg distintas y las 3 celdas de dividendos.
#impuesto tomado impuesto a cargo- ganancias ocasionales bm -bh

data=pd.read_csv(r"users/symlinks/baseline/data/recip-1/report_households_tmi.detail.2019.csv",index_col="measure")
data_trans=data.transpose()
utilidades=101596014000000
impuesto_empresas=36708319000000

divid=float(data_trans["income, dividend: sums"][0])
data_trans["percentage_dividend"]=data_trans.apply(lambda row:float(row["income, dividend: sums"])/divid ,axis=1)
data_trans["utilidades: sums"]=data_trans.apply(lambda row:row["percentage_dividend"]*utilidades,axis=1)
data_trans["tax empres: sums"]=data_trans.apply(lambda row:row["percentage_dividend"]*impuesto_empresas,axis=1)
data_trans["added income"]=data_trans.apply(lambda row: row["utilidades: sums"]+float(row["IT: sums"])-float(row["income, dividend: sums"]),axis=1)
data_trans["added tax"]=data_trans.apply(lambda row: row["tax empres: sums"]+float(row["tax: sums"]),axis=1)
data_trans["TET utilities/total_income"]=data_trans.apply(lambda row: row["tax empres: sums"]/row["added income"],axis=1)
data_trans["added tax/total_income"]=data_trans.apply(lambda row: row["added tax"]/row["added income"],axis=1)
data_trans["unimputed tax/pre_imp_income"]=data_trans.apply(lambda row: float(row["tax: sums"])/float(row["IT: sums"]),axis=1)


data_trans.to_csv(r"data/input_data.csv")

