from python.vat.build.classes import File, Correction
import numpy as np
import math


subsample = 10

folder = "data/enph-2017/recip-" + str(subsample) + "/"

variables = { "DIRECTORIO" : "household"
              , "ORDEN" : "household-member"
              , "FEX_C" : "weight"
}

# These apply to every file, be it purchases or people
corrections = [
  Correction.Replace_Substring_In_Column( "weight", ",", "." )
]
