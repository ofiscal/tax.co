In this email, David Suarez described portions of the ENIG 2007 and the ENPH 2017 relevant to the VAT analysis.


# ENIG 2007:

-Provides information the 24 principal cities, and the data can be aggregated for rural/urban households. 


## These are the datasets that contain revelant information for the VAT:

-Ig_ml_hogar: The table contains info regarding characteristics of dwellings and livelihoods. Question P5090 and P5100 ask if the households owns or rents the place and the value paid. Important since VAT applies to housing rents.



-Ig_gsdp_gas_dia: Contains information regarding daily expenditures for income earners in the household. The questions GDP_ARTCLO, GDP_CNTDAD_ADQRDA, GDP_FORMA_ADQSCION, GDP_LUGAR_COMPRA and GDP_VALOR_PGDO_ESTMDO represent a complete COICOP code for the article, the quantity, if they purchased the good (01 is the code for purchases), place of acquisition, and total estimated value, respectively. The variables that represent adjusted consumption and total payments by month: GDP_CNTDAD_ADQRDA_MES_AJST and GDP_VALOR_PGDO_ESTMDO_MES_AJST. 



-Ig_gsdu_gas_dia: Contains information regarding daily expenditures for urban households. The questions GDU_ARTCLO, GDU_CNTDAD_ADQRDA, GDU_FORMA_ADQSCION, GDU_LUGAR_COMPRA and GDU_VALOR_PGDO_ESTMDO represent a complete COICOP code for the article, the quantity, if they purchased the good (01 is the code for purchases), place of acquisition , and total estimated value, respectively. The variables that represent adjusted consumption and total payments by month: GDU_CNTDAD_ADQRDA_MES_AJST and GDU_VALOR_PGDO_ESTMDO_MES_AJST. 



-Ig_gssr_gas_sem: Contains information regarding weekly expenditures for rural households. The questions GSR_ARTCLO, GSR_CNTDAD_UDM_ESTANDAR, GSR_FORMA_ADQSCION, GSR_LUGAR_CMPRA, GSR_UDM_ESTANDAR, and  GSR_VALOR_PGDO_ESTMDO_MES represent a complete COICOP code for the article, the quantity, if they purchased the good (01 is the code for purchases), place (store, restaurant), measurement units for quantities and total estimated value per month, respectively. 



-Ig_gsmf_compra: This table contains info regarding purchases less-frequent expenditures. The questions GMF_CMPRA_ARTCLO, GMF_CMPRA_VLR_PAGO_MES, GMF_CMPRA_LUGAR and GMF_CMPRA_FRCNCIA, 

 represent a complete COICOP code for the good/service, the total amount paid per month, the place of the purchase and its frecuency, respectively.



- Ig_gssu_gasto_alimentos_cap_c and Ig_gssr_gasto_alimentos_cap_c: These tables contain food expenditures that were imputed for households that did not complete the booklets used to compile tables Ig_gsdu_gas_dia and Ig_gssr_gas_sem but reported to have made purchases in the reference period of the survey.  We can only recover prices for the former, using the questions ARTICULO (COICOP code), VALOR_MENSUAL_ALIMENTO, and CANTIDAD; for the latter only total monetary values are reported.



# ENPH 2017:

-Provides information for the 32 principal cities, 6 intermediate cities and 140 municipalities. Covers information for 90000 households.


## These are the datasets that contain relevant information for the VAT simulation:

SEA_ENC_GCFHR_CE_CSV: The table contains information of personal expenses for rural households. The questions NC2R_CE_P2, NC2R_CE_P4S1, NC2R_CE_P4S2, NC2R_CE_P5, NC2R_CE_P6, NC2R_CE_P7, and NC2R_CE_P8 represent a complete COICOP code for the article, the quantity, measurement units, if they purchased the good (01 is the code for purchases), place of acquisition, total estimated value and frequency of acquisition, respectively.
