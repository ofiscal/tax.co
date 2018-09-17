from python.vat.build.classes import File, Correction
from numpy import nan

subsample = 10
folder = "data/enph-2017/recip-" + str(subsample) + "/"
variables = { "DIRECTORIO" : "household"
              , "ORDEN" : "household-member"
              , "FEX_C" : "weight"
}
corrections = [
  Correction.Replace_Substring_In_Column( "weight", ",", "." )
]

quantity_corrections = [
  Correction.Replace_Substring_In_Column( "quantity", ",", "." )
  , Correction.Replace_Missing_Values( "quantity", 1 )
]

coicop_corrections = [
  # PTIFALL : Special treatment.
  # I would run this correction on each individual input file, for parallelism with
  # the other common corrections. But to do that I would have to first convert them from numeric to string,
  # whereas if I wait until they are appended, they will already have been converted.
  Correction.Replace_Entirely_If_Substring_Is_In_Column( "coicop", "inv", nan )
]

purchase_corrections = quantity_corrections
