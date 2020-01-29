import numpy as np

# Describes how to translate from ENPH frequency codes
# to a literal monthly frequency.
freq = {
    1  : (365.25/12) / 1   # 1  » Diario
  , 2  : (365.25/12) / 3.5 # 2  » Varias veces por semana
  , 3  : (365.25/12) / 7   # 3  » Semanal
  , 4  : (365.25/12) / 15  # 4  » Quincenal
  , 5  : 1 / 1             # 5  » Mensual
  , 6  : 1 / 2             # 6  » Bimestral
  , 7  : 1 / 3             # 7  » Trimestral
  , 8  : 1 / 12            # 8  » Anual
  , 9  : 1 / (3*12)        # 9  » Esporádica
  , 10 : 1 / 6             # 10 » Semestral
  , 11 : np.nan            # 11 » Nunca
}
