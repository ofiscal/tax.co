# At times this is memory intensive. My OS kept killing it, until I ran it with nothing else going on
# -- closed my browsers and all other docker containers. (I left Emacs, Dolphin and a few Konsoles open.)

import pandas as pd
import datafiles


## The 2017 ENIG survey

folder = datafiles.folder(2017)
names = datafiles.files[2017]

for name in names:
  print("now (henceforth) processing: " + name)
  data = pd.read_stata(folder + "orig-dta/" + name + '.dta')
  data_recip_10 =  data.sample(frac=0.1) 
  data_recip_10.to_csv(   folder + "recip-10/"   + name + '.csv')
  data_recip_100 =  data.sample(frac=0.01) 
  data_recip_100.to_csv(  folder + "recip-100/"  + name + '.csv')
  data_recip_1000 = data.sample(frac=0.001)
  data_recip_1000.to_csv( folder + "recip-1000/" + name + '.csv')


## The 2007 ENIG survey

folder = datafiles.folder(2007)
names = datafiles.files[2007]

for name in names:
  print("now (henceforth) processing: " + name)
  dtype_dict = {}
  # for the logic behind the next two lines, see format-investigations.py
  if   name == "Ig_ml_hogar":               dtype_dict = {'P5185S9A1': str}
  elif name == "Ig_ml_pblcion_edad_trbjar": dtype_dict = {'P7580S1': str}
  data = pd.read_csv( folder + "orig-txt/" + name + '.txt',
                      sep='\t', encoding='latin_1',
                      dtype = dtype_dict)
  data_recip_10 =  data.sample(frac=0.1) 
  data_recip_10.to_csv(   folder + "recip-10/"   + name + '.csv')
  data_recip_100 =  data.sample(frac=0.01) 
  data_recip_100.to_csv(  folder + "recip-100/"  + name + '.csv')
  data_recip_1000 = data.sample(frac=0.001)
  data_recip_1000.to_csv( folder + "recip-1000/" + name + '.csv')
