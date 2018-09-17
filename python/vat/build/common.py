from python.vat.build.classes import File, Correction


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
  Correction.Replace_Substring_In_Column( "weight", ",", "." )
  , Correction.Replace_Missing_Values( "weight", 1 )
]

purchase_corrections = quantity_corrections

